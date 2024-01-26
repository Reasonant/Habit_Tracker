
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
    except sqlite3.IntegrityError as IR:
        print(f"Error in create_habit() : {IR}")
        # print("Sorry, this habit name probably already exists. Try a new one.")
    except Exception as e:
        print(f"Error in create_habit(): {e}, type:{type(e)}")


def update_habit(db: sqlite3.Connection, habit_name: str, periodicity: str, task_specification: str):
    """
    A function to change a habit's attributes. (periodicity or task_specification).

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
    try:
        query = """DELETE FROM habits WHERE name = ?"""
        cursor.execute(query, (habit_name,))
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


def get_all_habits(db: sqlite3.Connection) -> list[tuple]:
    """
    A function used for retrieving a list of all stored habits.

    :param db: The database connection object.
    :return: A list of tuples. (NAME, PERIODICITY, TASK_SPECIFICATION, DATE_OF_CREATION).
    """
    cursor = db.cursor()
    query = """SELECT * FROM habits"""
    cursor.execute(query)
    db.commit()
    return cursor.fetchall()


def get_habit_records_by_name(db: sqlite3.Connection, habit_name: str) -> list[tuple]:
    """
    A function used for retrieving all the records of a given habit.

    :param db: The database connection object.
    :param habit_name: Name of the given habit for which to retrieve data.
    :return: A list of tuples. (DATE, NAME).
    """
    cursor = db.cursor()
    query = """SELECT * FROM records WHERE habit_name = ?"""
    try:
        cursor.execute(query, (habit_name,))
        db.commit()
        return cursor.fetchall()
    except Exception as e:
        print(f"Error in get_habit_records_by_name(): {e}, type:{type(e)}")


def get_all_habits_records(db: sqlite3.Connection) -> list[tuple]:
    """
    A function used for retrieving all records of all habits.

    :param db: The database connection object.
    :return: A list of tuples. (DATE, NAME).
    """
    cursor = db.cursor()
    query = """SELECT * FROM records """
    cursor.execute(query)
    db.commit()
    return cursor.fetchall()


def get_habits_by_periodicity(db: sqlite3.Connection, periodicity: str) -> list[tuple]:
    """
    A function used for retrieving all habits with the given periodicity.

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
