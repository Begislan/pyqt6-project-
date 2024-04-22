from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt

from .database import DataBase


# Карточка врача
class DoctorDialog(QtWidgets.QDialog):
    def __init__(
        self, db: DataBase, doctpr_id: int = None, parent: QtWidgets.QWidget = None
    ) -> None:
        super(DoctorDialog, self).__init__(parent)

        self.db = db
        self.doctor_id = doctpr_id
        self.setWindowTitle("Врач")
        self.name = QtWidgets.QLineEdit(self)
        self.name.setPlaceholderText("ФИО")

        self.birthday = QtWidgets.QDateEdit(self)
        self.birthday.setCalendarPopup(True)
        self.birthday.setDisplayFormat("dd.MM.yyyy")

        self.specialty = QtWidgets.QLineEdit(self)
        self.specialty.setPlaceholderText("Специальность")

        # self.phone = QtWidgets.QLineEdit(self)
        # self.phone.setPlaceholderText("Телефон")
        # self.phone.setInputMask("+7(999)999-99-99")

        self.add_button = QtWidgets.QPushButton()

        if self.doctor_id is not None:
            self.add_button.setText("Обновить")
            self.load_doctor_data()
        else:
            self.add_button.setText("Добавить")

        self.add_button.clicked.connect(self.process_doctor)
        self.layout = QtWidgets.QFormLayout(self)
        self.layout.addRow("ФИО", self.name)
        self.layout.addRow("Дата рождения", self.birthday)
        self.layout.addRow("Специальность", self.specialty)
        # self.layout.addRow("Телефон", self.phone)
        self.layout.addRow(self.add_button)

    # Загрузка данных врача
    def load_doctor_data(self):
        doctor_data = self.db.get_doctor(self.doctor_id)
        self.name.setText(doctor_data["name"])
        self.birthday.setDate(
            QtCore.QDate.fromString(doctor_data["date_of_birth"], "dd.MM.yyyy")
        )
        self.specialty.setText(doctor_data["speciality"])
        # self.phone.setText(doctor_data["phone"])

    # Добавление или обновление данных врача
    def process_doctor(self) -> None:
        if self.doctor_id is None:
            self.db.add_doctor(
                self.name.text(),
                self.birthday.date().toString("dd.MM.yyyy"),
                self.specialty.text(),
                # self.phone.text(),
            )
        else:
            self.db.update_doctor(
                self.doctor_id,
                self.name.text(),
                self.birthday.date().toString("dd.MM.yyyy"),
                self.specialty.text(),
                # self.phone.text(),
            )
        self.accept()
