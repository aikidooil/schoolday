import sqlite3
from datetime import datetime

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

    # метод для вставки нового предмета
    def insert_subject(self, name, teacher, room, capacity):
        date = datetime.now().strftime("%Y-%m-%d")
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
    def get_subjects(self):
        self.cursor.execute("""
            SELECT * FROM Subjects WHERE deleted = 0
        """)
        return self.cursor.fetchall()

    # проверка на наличие расписания
    def schedule_exists(self):
        self.cursor.execute("""
            SELECT COUNT(*) FROM Subjects WHERE deleted = 0
        """)
        return self.cursor.fetchone()[0] > 0

    # проверка на количество уроков у преподавателя
    def check_teacher(self, teacher):
        date = datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute("""
            SELECT COUNT(*) FROM Subjects WHERE teacher = ? AND date = ?
        """, (teacher, date))
        return self.cursor.fetchone()[0] < 5
