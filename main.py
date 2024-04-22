import sys

from PyQt6 import QtWidgets

from infosystem import AuthWindow, DataBase, MainWindow


def main():
    # Создание базы данных
    db = DataBase()
    # Создание приложения
    app = QtWidgets.QApplication(sys.argv)
    # Создание окна авторизации
    login = AuthWindow(db=db)
    # Отображение окна авторизации
    login.show()
    # Если авторизация прошла успешно, то открываем главное окно
    if login.exec() == QtWidgets.QDialog.DialogCode.Accepted:
        window = MainWindow(db=db)
        window.show()
        sys.exit(app.exec())
    else:
        # Иначе закрываем приложение
        sys.exit(0)


if __name__ == "__main__":
    main()
