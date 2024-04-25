from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt

from .database import DataBase


# Карточка пациента
class PatientDialog(QtWidgets.QDialog):
    def __init__(
        self, db: DataBase, patient_id: int = None, parent: QtWidgets.QWidget = None
    ) -> None:
        super(PatientDialog, self).__init__(parent)
        self.db = db
        self.patient_id = patient_id
        self.setWindowTitle("Пациент")
        self.name = QtWidgets.QLineEdit(self)
        self.name.setPlaceholderText("ФИО")

        self.birthday = QtWidgets.QDateEdit(self)
        self.birthday.setCalendarPopup(True)
        self.birthday.setDisplayFormat("dd.MM.yyyy")

        self.address = QtWidgets.QLineEdit(self)
        self.address.setPlaceholderText("город, улица, дом")

        self.phone = QtWidgets.QLineEdit(self)
        self.phone.setPlaceholderText("Телефон")
        self.phone.setInputMask("+996(999)99-99-99")

        self.sex = QtWidgets.QComboBox(self)
        self.sex.addItems(["М", "Ж"])
        self.add_button = QtWidgets.QPushButton()

        if self.patient_id is not None:
            self.add_button.setText("Обновить")
            self.load_patient_data()
        else:
            self.add_button.setText("Добавить")

        self.add_button.clicked.connect(self.process_patient)
        self.layout = QtWidgets.QFormLayout(self)
        self.layout.addRow("ФИО", self.name)
        self.layout.addRow("Дата рождения", self.birthday)
        self.layout.addRow("Адрес", self.address)
        self.layout.addRow("Телефон", self.phone)
        self.layout.addRow("Пол", self.sex)
        self.layout.addRow(self.add_button)

    # Загрузка данных пациента
    def load_patient_data(self):
        patient_data = self.db.get_patient(self.patient_id)
        self.name.setText(patient_data["name"])
        self.birthday.setDate(
            QtCore.QDate.fromString(patient_data["date_of_birth"], "dd.MM.yyyy")
        )
        self.address.setText(patient_data["address"])
        self.phone.setText(patient_data["phone"])
        self.sex.setCurrentText(patient_data["sex"])

    # Добавление или обновление данных пациента
    def process_patient(self) -> None:
        if self.patient_id is None:
            self.db.add_patient(
                self.name.text(),
                self.birthday.text(),
                self.address.text(),
                self.phone.text(),
                self.sex.currentText(),
            )
        else:
            self.db.update_patient(
                self.patient_id,
                self.name.text(),
                self.birthday.text(),
                self.address.text(),
                self.phone.text(),
                self.sex.currentText(),
            )
        self.accept()