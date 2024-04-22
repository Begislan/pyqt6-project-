import hashlib
import os
import sqlite3


# Класс для работы с базой данных SQLite
class DataBase:
    def __init__(self, db_path: str = "hospital.db") -> None:
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def add_patient(
        self, name: str, date_of_birth: str, address: str, phone: str, sex: str
    ) -> None:
        self.cursor.execute(
            """
            INSERT INTO Patients(name, date_of_birth, address, phone, sex)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name, date_of_birth, address, phone, sex),
        )
        self.connection.commit()

    # Добавление в базу данных нового пользователя
    def delete_patient(self, id: int) -> None:
        self.cursor.execute(
            """
            DELETE FROM Patients
            WHERE id = ?
            """,
            (id,),
        )
        self.connection.commit()

    # Удаление пользователя из базы данных
    def get_patient(self, id: int) -> dict:
        self.cursor.execute(
            """
            SELECT * FROM Patients
            WHERE id = ?
            """,
            (id,),
        )
        patient_data = self.cursor.fetchone()
        if patient_data is not None:
            columns = [column[0] for column in self.cursor.description]
            patient = {columns[i]: patient_data[i] for i in range(len(columns))}
            return patient
        else:
            return None

    # Получение данных о пользователе из базы данных
    def update_patient(
        self, id: int, name: str, date_of_birth: str, address: str, phone: str, sex: str
    ) -> None:
        self.cursor.execute(
            """
            UPDATE Patients
            SET name = ?, date_of_birth = ?, address = ?, phone = ?, sex = ?
            WHERE id = ?
            """,
            (name, date_of_birth, address, phone, sex, id),
        )
        self.connection.commit()

    # Обновление данных о пользователе в базе данных
    def get_patients(self, order_by: str = "name") -> list:
        self.cursor.execute(
            f"""
            SELECT * FROM Patients
            ORDER BY {order_by}
            """
        )
        return self.cursor.fetchall()

    # Получение списка врачей из базы данных
    def get_doctors(self, order_by: str = "name") -> list:
        self.cursor.execute(
            f"""
            SELECT * FROM Doctors
            ORDER BY {order_by}
            """
        )
        return self.cursor.fetchall()

    # Получение списка  врачей из базы данных
    def get_doctor(self, id: int) -> dict:
        self.cursor.execute(
            """
            SELECT * FROM Doctors
            WHERE id = ?
            """,
            (id,),
        )
        doctor_data = self.cursor.fetchone()
        if doctor_data is not None:
            columns = [column[0] for column in self.cursor.description]
            doctor = {columns[i]: doctor_data[i] for i in range(len(columns))}
            return doctor
        else:
            return None

    # Добавление в базу данных нового врача
    def add_doctor(
        self,
        name: str,
        date_of_birth,
        speciality: str,
    ) -> None:
        self.cursor.execute(
            """
            INSERT INTO Doctors(name, date_of_birth, speciality)
            VALUES (?, ?, ?)
            """,
            (name, date_of_birth, speciality),
        )
        self.connection.commit()

    # Удаление врача из базы данных
    def delete_doctor(self, id: int) -> None:
        self.cursor.execute(
            """
            DELETE FROM Doctors
            WHERE id = ?
            """,
            (id,),
        )
        self.connection.commit()

    # Обновление данных о враче в базе данных
    def update_doctor(
        self,
        id: int,
        name: str,
        date_of_birth: str,
        speciality: str,
    ) -> None:
        self.cursor.execute(
            """
            UPDATE Doctors
            SET name = ?, date_of_birth = ?, speciality = ?
            WHERE id = ?
            """,
            (name, date_of_birth, speciality, id),
        )
        self.connection.commit()

    # Получение списка записей на прием из базы данных
    def get_appointments(self, order_by: str = "appointment_date") -> list:
        self.cursor.execute(
            f"""
            SELECT * FROM Appointments
            ORDER BY {order_by}
            """
        )
        return self.cursor.fetchall()

    # Получение записи на прием из базы данных
    def get_appointment(self, id: int) -> dict:
        self.cursor.execute(
            """
            SELECT * FROM Appointments
            WHERE id = ?
            """,
            (id,),
        )
        appointment_data = self.cursor.fetchone()
        if appointment_data is not None:
            columns = [column[0] for column in self.cursor.description]
            appointment = {columns[i]: appointment_data[i] for i in range(len(columns))}
            return appointment
        else:
            return None

    # Добавление в базу данных новой записи на прием
    def add_appointment(
        self, date: str, time: str, patient_id: int, doctor_id: int
    ) -> None:
        self.cursor.execute(
            """
            INSERT INTO Appointments(appointment_date, time, patient_id, doctor_id)
            VALUES (?, ?, ?, ?)
            """,
            (date, time, patient_id, doctor_id),
        )
        self.connection.commit()

    # Удаление записи на прием из базы данных
    def delete_appointment(self, id: int) -> None:
        self.cursor.execute(
            """
            DELETE FROM Appointments
            WHERE id = ?
            """,
            (id,),
        )
        self.connection.commit()

    # Обновление данных о записи на прием в базе данных
    def update_appointment(
        self, id: int, date: str, time: str, patient_id: int, doctor_id: int
    ) -> None:
        self.cursor.execute(
            """
            UPDATE Appointments
            SET appointment_date = ?, time = ?, patient_id = ?, doctor_id = ?
            WHERE id = ?
            """,
            (date, time, patient_id, doctor_id, id),
        )
        self.connection.commit()

    # Получение списка записей на прием по пациенту из базы данных
    def get_appointments_by_patient(self, patient_id: int) -> list:
        self.cursor.execute(
            """
            SELECT * FROM Appointments
            WHERE patient_id = ?
            """,
            (patient_id,),
        )
        return self.cursor.fetchall()

    # Проверка пользователя в базе данных
    def check_user(self, username: str, password: str) -> bool:
        password = self._hash_password(password)
        self.cursor.execute(
            """
            SELECT * FROM Users
            WHERE username = ? AND password = ?
            """,
            (username, password),
        )
        return bool(self.cursor.fetchone())

    # Получение роли пользователя из базы данных
    def get_user_role(self, username: str) -> str:
        self.cursor.execute(
            """
            SELECT role FROM Users
            WHERE username = ?
            """,
            (username,),
        )
        return self.cursor.fetchone()[0]

    # Добавление в базу данных нового пользователя
    def add_user(self, username: str, password: str, role: str) -> None:
        password = self._hash_password(password)
        try:
            self.cursor.execute(
                """
                INSERT INTO Users(username, password, role)
                VALUES (?, ?, ?)
                """,
                (username, password, role),
            )
        except sqlite3.IntegrityError:
            raise ValueError("User already exists")
        self.connection.commit()

    # Хеширование пароля
    def _hash_password(self, password: str) -> str:
        return hashlib.md5(password.encode()).hexdigest()

    # Создание таблиц в базе данных
    def create_tables(self) -> None:
        self._create_patients()
        self._create_doctors()
        self._create_appointments()
        self._create_users()

    # Cоздание таблицы пациентов
    def _create_patients(self) -> None:
        self.cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS  Patients(
        id INTEGER PRIMARY KEY,
        name TEXT,
        date_of_birth TEXT,
        address TEXT,
        sex TEXT CHECK(sex IN('М', 'Ж')),
        phone TEXT
    )
"""
        )

    # Cоздание таблицы врачей
    def _create_doctors(self) -> None:
        self.cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS Doctors(
        id INTEGER PRIMARY KEY,
        name TEXT,
        date_of_birth TEXT,
        speciality TEXT
    )
            """
        )

    # Cоздание таблицы записей на прием
    def _create_appointments(self) -> None:
        self.cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS Appointments(
        id INTEGER PRIMARY KEY,
        patient_id INTEGER,
        doctor_id INTEGER,
        appointment_date TEXT,
        time TEXT,
        FOREIGN KEY (patient_id) REFERENCES Patients(id),
        FOREIGN KEY (doctor_id) REFERENCES Doctors(id)
    )
"""
        )

    # Cоздание таблицы пользователей
    def _create_users(self) -> None:
        self.cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT CHECK(role IN ('admin', 'user'))
    )
"""
        )
