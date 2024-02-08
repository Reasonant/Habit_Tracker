import sqlite3
from datetime import date, datetime, timedelta


def insert_initial_data(db: sqlite3.Connection):
    """
    This function appends the initial data to the database.
    It appends 5 habits and for each habit it appends a tracking period of 4 weeks into records.

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

    habits_records = []
    four_weeks_back = datetime.now().date() - timedelta(weeks=4)
    regular_exercise_tracking_days = [0, 5, 11, 17, 21, 28]
    digital_detox_tracking_days = [0, 7, 14, 21, 28]

    data_regular_exercise = [str(four_weeks_back + timedelta(days=i)) for i in regular_exercise_tracking_days]
    habits_records.append(data_regular_exercise)

    data_healthy_eating = [str(four_weeks_back + timedelta(days=i)) for i in range(5)]
    data_healthy_eating.extend([str(four_weeks_back + timedelta(days=7))])
    data_healthy_eating.extend([str(four_weeks_back + timedelta(days=i)) for i in range(9, 15)])
    data_healthy_eating.extend([str(four_weeks_back + timedelta(days=17))])
    data_healthy_eating.extend([str(four_weeks_back + timedelta(days=i)) for i in range(18, 29)])
    habits_records.append(data_healthy_eating)

    data_meditation = [str(four_weeks_back + timedelta(days=i)) for i in range(16)]
    data_meditation.extend([str(four_weeks_back + timedelta(days=18))])
    data_meditation.extend([str(four_weeks_back + timedelta(days=i)) for i in range(19, 29)])
    habits_records.append(data_meditation)

    data_quality_sleep_routine = [str(four_weeks_back + timedelta(days=i)) for i in range(14)]
    data_quality_sleep_routine.extend([str(four_weeks_back + timedelta(days=20))])
    data_quality_sleep_routine.extend([str(four_weeks_back + timedelta(days=i)) for i in range(21, 29)])
    habits_records.append(data_quality_sleep_routine)

    data_digital_detox = [str(four_weeks_back + timedelta(days=i)) for i in digital_detox_tracking_days]
    habits_records.append(data_digital_detox)

    for name, periodicity, task_specification in zip(habits_names, habits_periodicity, habits_tasks):
        query = """INSERT OR IGNORE INTO habits VALUES (?,?,?,?)"""
        try:
            cursor.execute(query, (name, periodicity, task_specification, str(four_weeks_back)))
        except sqlite3.IntegrityError:
            print(f"{name} already exists.")

    query = """INSERT OR IGNORE INTO records VALUES (?,?)"""
    for habit, records in zip(habits_names, habits_records):
        for event_date in records:
            try:
                cursor.execute(query, (event_date, habit))
            except sqlite3.Error as e:
                print(f"Error in insert_initial_data(): {e}")
    db.commit()


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
    except sqlite3.Error as e:
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
    try:
        cursor.execute(query, (periodicity, task_specification, habit_name))
        db.commit()
    except sqlite3.Error as e:
        print(f"Error in update_habit(): {e}, {type(e)}")


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
        db.commit()
        print("Habit deleted !")
    except sqlite3.Error as e:
        print(f"Error in delete_habit(): {e}, {type(e)}")


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
        print("This record already exists.")
    else:
        if not event_date:
            event_date = str(date.today())
        query = """INSERT INTO records VALUES (?,?)"""
        cursor.execute(query, (event_date, name))
        db.commit()
        print("Task recorded successfully !")


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
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error in get_all_habits(): {e}, {type(e)}")


def get_habit_records_by_name(db: sqlite3.Connection, habit_name: str) -> list[tuple]:
    """
    A function used to retrieve all records of a given habit.

    :param db: The database connection object.
    :param habit_name: Name of the given habit for which to retrieve data.
    :return: A list of tuples. (DATE, ).
    """
    cursor = db.cursor()
    query = """SELECT date FROM records WHERE habit_name = ?"""
    try:
        cursor.execute(query, (habit_name,))
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"(Error in get_habit_records_by_name(): {e}, {type(e)}")


def get_all_habits_records(db: sqlite3.Connection) -> list[tuple]:
    """
    A function used to retrieve all records of all habits.

    :param db: The database connection object.
    :return: A list of tuples. (DATE, ).
    """
    cursor = db.cursor()
    query = """SELECT date FROM records """
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error in get_all_habits_records(): {e}, {type(e)}")


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
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error in get_habits_by_periodicity(): {e}, type:{type(e)}")
