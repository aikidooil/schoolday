import sqlite3
from datetime import date
import random

class Database:
    # класс для управления операциями базы данных
    def __init__(self):
        self.conn = sqlite3.connect('db/basic/school.db')
        self.cursor = self.conn.cursor()
        self.create_tables()

    # метод для создания таблиц
    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Subjects (
                id INTEGER PRIMARY KEY,
                name TEXT,
                teacher TEXT,
                room INTEGER,
                capacity INTEGER,
                deleted INTEGER DEFAULT 0,
                date TEXT
            )
        """)
        self.conn.commit()
        self.create_rooms_table()

    # метод для создания таблицы кабинетов
    def create_rooms_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Rooms (
                room INTEGER PRIMARY KEY,
                capacity INTEGER
            )
        """)
        self.conn.commit()
        self.create_rooms()

    # создание кабинетов и выбор вместимости кабинетов
    def create_rooms(self):
        for i in range(1, 151):
            capacity = random.randint(20, 30)
            self.cursor.execute("SELECT room FROM Rooms WHERE room = ?", (i,))
            room = self.cursor.fetchone()
            if room is None:
                self.cursor.execute("""
                    INSERT INTO Rooms (room, capacity) VALUES (?, ?)
                """, (i, capacity))
            self.conn.commit()

    # метод для вставки нового предмета
    def insert_subject(self, name, teacher, room, capacity, date):
        self.cursor.execute("""
            INSERT INTO Subjects (name, teacher, room, capacity, date) VALUES (?, ?, ?, ?, ?)
        """, (name, teacher, room, capacity, date))
        self.conn.commit()

    # метод для удаления предмета с помощью id
    def delete_subject_by_id(self, id):
        self.cursor.execute("""
            UPDATE Subjects SET deleted = 1 WHERE id = ?
        """, (id,))
        self.conn.commit()

    # метод для удаления предмета с помощью названия
    def delete_subject_by_name(self, name):
        self.cursor.execute("""
            UPDATE Subjects SET deleted = 1 WHERE name = ?
        """, (name,))
        self.conn.commit()

    # получение всех предметов
    def get_subjects(self, date):
        self.cursor.execute("""
            SELECT * FROM Subjects WHERE deleted = 0 AND date = ?
        """, (date,))
        return self.cursor.fetchall()

    # получение всех дат
    def get_dates(self):
        self.cursor.execute("""
            SELECT DISTINCT date FROM Subjects WHERE deleted = 0
        """)
        return self.cursor.fetchall()

    # проверка на наличие расписания
    def schedule_exists(self):
        self.cursor.execute("""
            SELECT COUNT(*) FROM Subjects WHERE deleted = 0
        """)
        return self.cursor.fetchone()[0] > 0

    # проверка на количество уроков у преподавателя
    def check_teacher(self, teacher, date):
        self.cursor.execute("""
            SELECT COUNT(*) FROM Subjects WHERE teacher = ? AND date = ?
        """, (teacher, date))
        return self.cursor.fetchone()[0] < 5

    # получение вместимости
    def get_room_capacity(self, room):
        self.cursor.execute("""
            SELECT capacity FROM Rooms WHERE room = ?
        """, (room,))
        return self.cursor.fetchone()[0]

    # получение сегодняшней даты
    def get_today_date(self):
        return date.today().strftime("%Y-%m-%d")

    # метод для получения доступных расписаний
    def get_schedules(self):
        self.cursor.execute("""
            SELECT DISTINCT date FROM Subjects WHERE deleted = 0
        """)
        return self.cursor.fetchall()