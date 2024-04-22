from PyQt6 import QtGui, QtWidgets
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QTextEdit

from .appointment_dialog import AppointmentDialog
from .database import DataBase
from .doctor_card import DoctorDialog
from .patient_card import PatientDialog


# Класс главного окна информационной системы
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, db: DataBase, parent=None) -> None:
        super(MainWindow, self).__init__(parent)
        self.db = db
        self.setWindowTitle('Разработка информационной системы по учёту пациентов больницы в среде программирования Python')
        self.setFixedSize(800, 600)
        self.tabbox = QtWidgets.QTabWidget(self)

        self.tabbox.addTab(self._create_patients_tab(), "Пациенты")
        self.setCentralWidget(self.tabbox)
        self.update_patients_table()

        self.tabbox.addTab(self._create_doctors_tab(), "Врачи")
        self.update_doctors_table()

        self.tabbox.addTab(self._create_appointments_tab(), "Записи")
        self.update_appointments_table()

        self.   tabbox.addTab(self._about(), "О программе")


    # О программе
    def _about(self) -> QWidget:
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()

        # Создаем QTextEdit с вашим текстом
        about_text = QTextEdit()
        about_text.setPlainText("Акматалиев Камчыбек Капарович - ПОВ(б)-1-20")
        about_text.setReadOnly(True)  # чтобы текст был доступен только для чтения

        layout.addWidget(about_text)
        tab.setLayout(layout)
        return tab

    # Создание вкладки "Врачи"
    def _create_doctors_tab(self) -> QWidget:
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self._create_doctors_table())
        layout.addWidget(self._create_doctors_buttons())
        tab.setLayout(layout)
        return tab

    # Создание таблицы "Врачи"
    def _create_doctors_table(self) -> QtWidgets.QTableView:
        self.model_doctor = QtGui.QStandardItemModel(self)
        self.model_doctor.setHorizontalHeaderLabels(
            ["ID", "ФИО", "Дата рождения", "Специальность"]
        )
        self.table_doctor = QtWidgets.QTableView()
        self.table_doctor.setModel(self.model_doctor)
        self.table_doctor.doubleClicked.connect(self._open_doctor)
        return self.table_doctor

    # Создание кнопок "Врачи"
    def _create_doctors_buttons(self) -> QtWidgets.QWidget:
        buttons = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self._create_add_doctor_button())
        layout.addWidget(self._create_delete_doctor_button())
        buttons.setLayout(layout)
        return buttons

    # Создание кнопки "Добавить"
    def _create_add_doctor_button(self) -> QtWidgets.QPushButton:
        button = QtWidgets.QPushButton("Добавить")
        button.clicked.connect(self._add_doctor)
        return button

    # Создание кнопки "Удалить"
    def _create_delete_doctor_button(self) -> QtWidgets.QPushButton:
        button = QtWidgets.QPushButton("Удалить")
        button.clicked.connect(self._delete_doctor)
        return button

    # Добавление врача
    def _add_doctor(self) -> None:
        dialog = DoctorDialog(db=self.db)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            self.update_doctors_table()

    # Удаление врача
    def _delete_doctor(self) -> None:
        id = (
            self.table_doctor.model()
            .index(self.table_doctor.currentIndex().row(), 0)
            .data()
        )
        self.db.delete_doctor(id)
        self.update_doctors_table()

    # Открытие карточки врача
    def _open_doctor(self) -> None:
        id = (
            self.table_doctor.model()
            .index(self.table_doctor.currentIndex().row(), 0)
            .data()
        )
        dialog = DoctorDialog(db=self.db, doctpr_id=id)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            self.update_doctors_table()

    # Обновление таблицы "Врачи"
    def update_doctors_table(self) -> None:
        self.model_doctor.clear()
        self.model_doctor.setHorizontalHeaderLabels(
            ["ID", "ФИО", "Дата рождения", "Специальность"]
        )
        doctors = self.db.get_doctors()
        for doctor in doctors:
            id, name, birthday, speciality = doctor
            row = [
                QtGui.QStandardItem(str(id)),
                QtGui.QStandardItem(name),
                QtGui.QStandardItem(birthday),
                QtGui.QStandardItem(speciality),
            ]

            self.model_doctor.appendRow(row)

    # Создание вкладки "Пациенты"
    def _create_patients_tab(self) -> QWidget:
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self._create_patients_table())
        layout.addWidget(self._create_patients_buttons())
        tab.setLayout(layout)
        return tab

    # Создание таблицы "Пациенты"
    def _create_patients_table(self) -> QtWidgets.QTableView:
        self.model_patient = QtGui.QStandardItemModel(self)
        self.model_patient.setHorizontalHeaderLabels(
            ["ID", "ФИО", "Дата рождения", "Адрес", "Пол", "Номер телефона"]
        )
        self.table_patient = QtWidgets.QTableView()
        self.table_patient.setModel(self.model_patient)
        # self.table_patient.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.)
        self.table_patient.doubleClicked.connect(self._open_patient)
        return self.table_patient

    # Создание кнопок "Пациенты"
    def _create_patients_buttons(self) -> QtWidgets.QWidget:
        buttons = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self._create_add_patient_button())
        layout.addWidget(self._create_delete_patient_button())
        buttons.setLayout(layout)
        return buttons

    # Создание кнопки "Добавить пациента"
    def _create_add_patient_button(self) -> QtWidgets.QPushButton:
        button = QtWidgets.QPushButton("Добавить пациента")
        button.clicked.connect(self._add_patient)
        return button

    # Создание кнопки "Удалить пациента"
    def _create_delete_patient_button(self) -> QtWidgets.QPushButton:
        button = QtWidgets.QPushButton("Удалить пациента")
        button.clicked.connect(self._delete_patient)
        return button

    # Добавление пациента
    def _add_patient(self) -> None:
        dialog = PatientDialog(self.db)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            self.update_patients_table()

    # Удаление пациента
    def _delete_patient(self) -> None:
        id = (
            self.table_patient.model()
            .index(self.table_patient.currentIndex().row(), 0)
            .data()
        )
        self.db.delete_patient(id)
        self.update_patients_table()

    # Открытие карточки пациента
    def _open_patient(self) -> None:
        id = (
            self.table_patient.model()
            .index(self.table_patient.currentIndex().row(), 0)
            .data()
        )
        dialog = PatientDialog(self.db, id)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            self.update_patients_table()

    # Обновление таблицы "Пациенты"
    def update_patients_table(self) -> None:
        self.model_patient.clear()
        self.model_patient.setHorizontalHeaderLabels(
            ["ID", "ФИО", "Дата рождения", "Адрес", "Пол", "Номер телефона"]
        )
        for patient in self.db.get_patients():
            id, name, date_of_birth, address, phone, sex = patient
            row = [
                QtGui.QStandardItem(str(id)),
                QtGui.QStandardItem(name),
                QtGui.QStandardItem(date_of_birth),
                QtGui.QStandardItem(address),
                QtGui.QStandardItem(phone),
                QtGui.QStandardItem(sex),
            ]
            self.model_patient.appendRow(row)
        self.table_patient.setModel(self.model_patient)

    # Создание вкладки "Приемы"
    def _create_appointments_tab(self) -> QWidget:
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self._create_appointments_table())
        layout.addWidget(self._create_appointments_buttons())
        tab.setLayout(layout)
        return tab

    # Создание таблицы "Приемы"
    def _create_appointments_table(self) -> QtWidgets.QTableView:
        self.model_appointment = QtGui.QStandardItemModel(self)
        self.model_appointment.setHorizontalHeaderLabels(
            ["ID", "Дата", "Время", "Пациент", "Врач"]
        )
        self.table_appointments = QtWidgets.QTableView()
        self.table_appointments.setModel(self.model_appointment)
        self.table_appointments.doubleClicked.connect(self._open_appointment)
        return self.table_appointments

    # Создание кнопок "Приемы"
    def _create_appointments_buttons(self) -> QtWidgets.QWidget:
        buttons = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self._create_add_appointment_button())
        layout.addWidget(self._create_delete_appointment_button())
        buttons.setLayout(layout)
        return buttons

    # Создание кнопки "Добавить прием"
    def _create_add_appointment_button(self) -> QtWidgets.QPushButton:
        button = QtWidgets.QPushButton("Добавить")
        button.clicked.connect(self._add_appointment)
        return button

    # Создание кнопки "Удалить прием"
    def _create_delete_appointment_button(self) -> QtWidgets.QPushButton:
        button = QtWidgets.QPushButton("Удалить")
        button.clicked.connect(self._delete_appointment)
        return button

    # Добавление приема
    def _add_appointment(self) -> None:
        dialog = AppointmentDialog(db=self.db)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            self.update_appointments_table()

    # Удаление приема
    def _delete_appointment(self) -> None:
        id = (
            self.table_appointments.model()
            .index(self.table_appointments.currentIndex().row(), 0)
            .data()
        )
        self.db.delete_appointment(id)
        self.update_appointments_table()

    # Открытие карточки приема
    def _open_appointment(self) -> None:
        id = (
            self.table_appointments.model()
            .index(self.table_appointments.currentIndex().row(), 0)
            .data()
        )
        dialog = AppointmentDialog(self.db, id)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            self.update_appointments_table()

    # Обновление таблицы "Приемы"
    def update_appointments_table(self) -> None:
        self.model_appointment.clear()
        self.model_appointment.setHorizontalHeaderLabels(
            ["ID", "Пациент", "Доктор", "Дата", "Время"]
        )
        for appointment in self.db.get_appointments():
            id, patient, doctor, date, time = appointment
            patient = self.db.get_patient(patient)["name"]
            doctor = self.db.get_doctor(doctor)["name"]
            row = [
                QtGui.QStandardItem(str(id)),
                QtGui.QStandardItem(patient),
                QtGui.QStandardItem(doctor),
                QtGui.QStandardItem(date),
                QtGui.QStandardItem(time),
            ]
            self.model_appointment.appendRow(row)
        self.table_appointments.setModel(self.model_appointment)
