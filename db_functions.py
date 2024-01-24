import sqlite3
from datetime import date


class DBFunctions:
    def __init__(self, database_filename):
        self.database_filename = database_filename
        self.db = sqlite3.connect(database_filename)
        self.cursor = self.db.cursor()

    def create_habit(self, name: str, periodicity: str, task_specification: str,
                     date_of_creation: str):
        query = """INSERT INTO habits VALUES (?,?,?,?)"""
        try:
            self.cursor.execute(query, (name, periodicity, task_specification, date_of_creation))
            self.db.commit()
        except Exception as e:
            print(f"Error: {e}")

    def update_habit(self, habit_name, periodicity, task_specification):
        query = """UPDATE habits SET periodicity = ?, task_specification = ? WHERE name = ?"""
        self.cursor.execute(query, (periodicity, task_specification, habit_name))
        self.db.commit()

    def delete_habit(self, habit_name):
        query = """DELETE FROM habits WHERE name = ?"""
        self.cursor.execute(query, (habit_name,))
        self.db.commit()

    def record_completed_task(self, name: str, event_date: str = None):
        if not event_date:
            event_date = str(date.today())
        query = """INSERT OR IGNORE INTO records VALUES (?,?)"""
        self.cursor.execute(query, (event_date, name))
        self.db.commit()

    def get_all_habits(self):
        query = """SELECT * FROM habits"""
        self.cursor.execute(query)
        self.db.commit()
        return self.cursor.fetchall()

    def get_habit_records_by_name(self, habit_name):
        query = """SELECT * FROM records WHERE name = ?"""
        try:
            self.cursor.execute(query, (habit_name,))
            self.db.commit()
            return self.cursor.fetchall()
        except Exception as e:
            return f"Error: {e}"

    def get_all_habits_records(self):
        query = """SELECT * FROM records """
        self.cursor.execute(query)
        self.db.commit()
        return self.cursor.fetchall()

    def get_habits_by_periodicity(self, periodicity):
        query = """SELECT * FROM habits WHERE periodicity = ?"""
        try:
            self.cursor.execute(query, (periodicity,))
            self.db.commit()
            return self.cursor.fetchall()
        except Exception as e:
            return f"Error: {e}"
        