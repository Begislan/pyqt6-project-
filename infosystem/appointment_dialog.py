from PyQt6 import QtCore, QtWidgets

from .database import DataBase


# Класс для добавления/обновления записи пациента к врачу
class AppointmentDialog(QtWidgets.QDialog):
    def __init__(
        self, db: DataBase, appointment_id: int = None, parent: QtWidgets.QWidget = None
    ) -> None:
        super(AppointmentDialog, self).__init__(parent)

        self.db = db
        self.appointment_id = appointment_id
        self.setWindowTitle("Запись")
        self.patient = QtWidgets.QComboBox(self)

        self._get_list_of_patients()
        self.doctor = QtWidgets.QComboBox(self)
        self._get_list_of_doctors()
        self.date = QtWidgets.QDateEdit(self)
        self.date.setCalendarPopup(True)
        self.date.setDisplayFormat("dd.MM.yyyy")
        self.time = QtWidgets.QTimeEdit(self)
        self.time.setDisplayFormat("HH:mm")
        self.add_button = QtWidgets.QPushButton()

        if self.appointment_id is not None:
            self.add_button.setText("Обновить")
            self.load_appointment_data()
        else:
            self.add_button.setText("Добавить")

        self.add_button.clicked.connect(self.process_appointment)
        self.layout = QtWidgets.QFormLayout(self)
        self.layout.addRow("Пациент", self.patient)
        self.layout.addRow("Врач", self.doctor)
        self.layout.addRow("Дата", self.date)
        self.layout.addRow("Время", self.time)
        self.layout.addRow(self.add_button)

    # Получение списка пациентов
    def _get_list_of_patients(self) -> None:
        patients = self.db.get_patients()
        for patient in patients:
            self.patient.addItem(patient[1], patient[0])

    # Получение списка врачей
    def _get_list_of_doctors(self) -> None:
        doctors = self.db.get_doctors()
        for doctor in doctors:
            self.doctor.addItem(doctor[1], doctor[0])

    # Загрузка данных о записи
    def load_appointment_data(self):
        appointment_data = self.db.get_appointment(self.appointment_id)
        self.patient.setCurrentIndex(
            self.patient.findData(int(appointment_data["patient_id"]))
        )
        self.doctor.setCurrentIndex(
            self.doctor.findData(int(appointment_data["doctor_id"]))
        )
        self.date.setDate(
            QtCore.QDate.fromString(appointment_data["appointment_date"], "dd.MM.yyyy")
        )
        self.time.setTime(QtCore.QTime.fromString(appointment_data["time"], "HH:mm"))

    # Добавление/обновление записи
    def process_appointment(self) -> None:
        if self.appointment_id is None:
            self.db.add_appointment(
                date=self.date.date().toString("dd.MM.yyyy"),
                time=self.time.time().toString("HH:mm"),
                patient_id=self.patient.currentData(),
                doctor_id=self.doctor.currentData(),
            )
        else:
            self.db.update_appointment(
                id=self.appointment_id,
                date=self.date.date().toString("dd.MM.yyyy"),
                time=self.time.time().toString("HH:mm"),
                patient_id=self.patient.currentData(),
                doctor_id=self.doctor.currentData(),
            )
        self.accept()