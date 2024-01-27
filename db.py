import sqlite3
from datetime import date


def create_tables(db: sqlite3.Connection):
    """
    Creates two tables in the database which we created above.
    Tables are:
        habits
        records

    :param db: The database connection object. Received from the caller (create_database())
    :return: None
    """
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


def insert_initial_data(db: sqlite3.Connection):
    """
    This function appends the initial data to the database.
    It appends 5 habits.

    :param db: The database connection object. Received from the caller (create_database())
    :return: None
    """
    cursor = db.cursor()
    habits_names = ["Regular Exercise",
                    "Healthy Eating",
                    "Meditation",
                    "Quality Sleep Routine",
                    "Digital Detox"]
    habits_periodicity = ["WEEKLY",
                          "DAILY",
                          "DAILY",
                          "DAILY",
                          "WEEKLY"]
    habits_tasks = ["Exercise",
                    "Eat a healthy meal",
                    "Meditate",
                    "Sleep at fixed time",
                    "Remove all digital devices"]
    habits_records = [["2021-01-12", "2021-01-13", "2021-01-14", "2021-01-15", "2021-01-19"],
                      ["2021-02-16", "2021-02-17"],
                      ["2022-04-24", "2022-04-26", "2022-04-27", "2022-04-28", "2022-06-02"],
                      ["2021-05-05", "2021-05-06", "2021-05-07", "2021-05-13", "2021-05-14", "2021-05-15"],
                      ["2023-01-02", "2023-01-03", "2023-01-04", "2023-01-15", "2023-01-16", "2023-01-17", "2023-01-18"]]
    for name, periodicity, task_specification in zip(habits_names, habits_periodicity, habits_tasks):
        query = """INSERT OR IGNORE INTO habits VALUES (?,?,?,?)"""
        try:
            cursor.execute(query, (name, periodicity, task_specification, str(date.today())))
            db.commit()
        except sqlite3.IntegrityError:
            print("This habit already exists.")
        except Exception as e:
            print(f"Error in insert_initial_data(): {e}, {type(e)}")

        for habit, records in zip(habits_names, habits_records):
            for event_date in records:
                record_completed_task(db, habit, event_date)
    db.commit()


def create_database(database_name: str = 'main.db'):
    """
    This function checks if a database file exists in the same directory as this file.
    If it does not exist then it creates it.
    It creates the tables and inserts initial data.

    :param database_name: The name of the database to create.
    :return: A sqlite3.Connection object
    """
    db = sqlite3.connect(database_name)
    create_tables(db)
    insert_initial_data(db)
    return db


def create_habit(db: sqlite3.Connection, name: str, periodicity: str,
                 task_specification: str, date_of_creation: str):
    """
    This function creates a new habit in the database.

    :param db: The database connection object.
    :param name: The name of the new habit.
    :param periodicity: The tracking period of the new habit.
    :param task_specification: The task specification of a habit (a description of the habit).
    :param date_of_creation: The date this habit is created.
    :return: None
    """
    cursor = db.cursor()
    query = """INSERT INTO habits VALUES (?,?,?,?)"""
    try:
        cursor.execute(query, (name, periodicity, task_specification, date_of_creation))
        db.commit()
    except sqlite3.IntegrityError:
        print("This habit already exists.")
    except Exception as e:
        print(f"Error in create_habit(): {e}, type:{type(e)}")


def update_habit(db: sqlite3.Connection, habit_name: str, periodicity: str, task_specification: str):
    """
    A function used to change a habit's attributes. (periodicity or task_specification).

    :param db: The database connection object.
    :param db: The database connection object.
    :param habit_name: The habit's name to change attributes.
    :param periodicity: New periodicity value.
    :param task_specification: New task_specification value.
    :return: None
    """
    cursor = db.cursor()
    query = """UPDATE habits SET periodicity = ?, task_specification = ? WHERE name = ?"""
    cursor.execute(query, (periodicity, task_specification, habit_name))
    db.commit()


def delete_habit(db: sqlite3.Connection, habit_name: str):
    """
    A function used to delete a stored habit.

    :param db: The database connection object.
    :param habit_name: The name of the habit to delete.
    :return: None
    """
    cursor = db.cursor()
    query = """DELETE FROM habits WHERE name = ?"""
    query_2 = """DELETE FROM records WHERE habit_name = ?"""
    try:
        cursor.execute(query, (habit_name,))
        cursor.execute(query_2, (habit_name,))
        print("Habit deleted !")
    except Exception as e:
        print(f"Error in delete_habit(): {e}, {type(e)}")
    db.commit()


def record_completed_task(db: sqlite3.Connection, name: str, event_date: str = None):
    """
    A function used to record the progress of a user for the given habit.

    :param db: The database connection object.
    :param name: The name of the habit to record progress.
    :param event_date: The date which the task was completed (Form : "YYYY-MM-DD").
    :return: None
    """
    cursor = db.cursor()
    query = "SELECT * from records WHERE date = ? AND habit_name = ?"
    if not event_date:
        event_date = str(date.today())
    cursor.execute(query, (event_date, name))
    existing_record = cursor.fetchone()
    if existing_record:
        # print("This record already exists.")
        pass
    else:
        if not event_date:
            event_date = str(date.today())
        query = """INSERT INTO records VALUES (?,?)"""
        cursor.execute(query, (event_date, name))
        db.commit()
        # print("Task recorded successfully !")


def get_habit(db: sqlite3.Connection, name: str) -> tuple:
    """
    A function used to retrieve data of a single habit.

    :param db: A sqlite3.Connection object
    :param name: The name of the habit to retrieve
    :return: A tuple of the habit's data
    """
    cursor = db.cursor()
    query = """SELECT * FROM habits where name = ?"""
    try:
        cursor.execute(query, (name,))
        return cursor.fetchone()
    except sqlite3.Error as e:
        print(f"Error in get_habit(): {e}, {type(e)}")


def get_all_habits(db: sqlite3.Connection) -> list[tuple]:
    """
    A function used to retrieve a list of all stored habits.

    :param db: The database connection object.
    :return: A list of tuples. (NAME, PERIODICITY, TASK_SPECIFICATION, DATE_OF_CREATION).
    """
    cursor = db.cursor()
    query = """SELECT * FROM habits"""
    cursor.execute(query)
    db.commit()
    return cursor.fetchall()


def get_habit_records_by_name(db: sqlite3.Connection, habit_name: str) -> list[tuple] | None:
    """
    A function used to retrieve all records of a given habit.

    :param db: The database connection object.
    :param habit_name: Name of the given habit for which to retrieve data.
    :return: A list of tuples. (DATE, NAME).
    """
    cursor = db.cursor()
    query = """SELECT date FROM records WHERE habit_name = ?"""
    try:
        cursor.execute(query, (habit_name,))
        db.commit()
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"(get_habit_records_by_name(): {e}")
        return None


def get_all_habits_records(db: sqlite3.Connection) -> list[tuple]:
    """
    A function used to retrieve all records of  habits.

    :param db: The database connection object.
    :return: A list of tuples. (DATE, ).
    """
    cursor = db.cursor()
    query = """SELECT date FROM records """
    cursor.execute(query)
    db.commit()
    return cursor.fetchall()


def get_habits_by_periodicity(db: sqlite3.Connection, periodicity: str) -> list[tuple]:
    """
    A function used to retrieve all records of habits with the given periodicity.

    :param db: The database connection object.
    :param periodicity: The periodicity of the habits' to return. (DAILY or WEEKLY)
    :return: A list of tuples. (NAME, PERIODICITY, TASK_SPECIFICATION, DATE_OF_CREATION).
    """
    cursor = db.cursor()
    query = """SELECT * FROM habits WHERE periodicity = ?"""
    try:
        cursor.execute(query, (periodicity,))
        db.commit()
        return cursor.fetchall()
    except Exception as e:
        print(f"Error in get_habits_by_periodicity(): {e}, type:{type(e)}")
