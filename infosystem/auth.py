from PyQt6 import QtWidgets

from .database import DataBase


#  Окно авторизации в систему
class AuthWindow(QtWidgets.QDialog):
    def __init__(self, db: DataBase, parent: QtWidgets.QWidget = None) -> None:
        super(AuthWindow, self).__init__(parent)
        self.db = db
        self.setWindowTitle("Авторизация в информационную систему пациентов")
        self.setFixedSize(300, 150)

        self.username = QtWidgets.QLineEdit(self)
        self.username.setPlaceholderText("Логин")
        self.password = QtWidgets.QLineEdit(self)
        self.password.setPlaceholderText("Пароль")
        self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.buttonlogin = QtWidgets.QPushButton("Войти", self)
        self.buttonlogin.clicked.connect(self.click_btn_login)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(self.buttonlogin)

    # Проверка логина и пароля
    def check_password(self) -> None:
        username = self.username.text()
        password = self.password.text()
        if self.db.check_user(username, password):
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")

    # Нажатие кнопки "Войти"
    def click_btn_login(self) -> None:
        self.check_password()
