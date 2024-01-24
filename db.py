import sqlite3
from datetime import date
import os
from db_functions import DBFunctions


def create_tables(database_name):
    """
    Creates two tables in the database which we created above.
    Tables are:
        habits
        records
    """
    db = sqlite3.connect(database_name)
    cursor = db.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS habits(
            name TEXT PRIMARY KEY,
            periodicity TEXT,
            task_specification TEXT,
            date_of_creation TEXT)""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS records(
            date TEXT,
            habit_name TEXT,
            FOREIGN KEY (habit_name) REFERENCES habits(name))""")

    db.commit()
    db.close()


def insert_initial_data(database_name):
    dbf = DBFunctions(database_name)
    habits_names = ["Regular Exercise", "Healthy Eating",
                    "Meditation", "Quality Sleep Routine", "Digital Detox"]
    habits_periodicity = ["weekly", "daily", "daily", "daily", "weekly"]
    habits_tasks = ["Exercise", "Eat a healthy meal", "Meditate",
                    "Sleep at fixed time", "Remove all digital devices"]
    for name, periodicity, task_specification in zip(habits_names, habits_periodicity, habits_tasks):
        dbf.create_habit(name, periodicity, task_specification, str(date.today()))


def create_database(database_name='main.db'):
    """
    Checks if a database file exists in the same directory as this file.
    If it does not exist then it creates it.
    """
    this_script_directory = os.path.dirname(os.path.abspath(__file__))
    filepath_name = os.path.join(this_script_directory, database_name)

    if not os.path.exists(filepath_name):
        db = sqlite3.connect(database_name)
        db.commit()
        db.close()
        print("Database created successfully")

        create_tables(database_name)
        insert_initial_data(database_name)
    else:
        print("Database already exists")
