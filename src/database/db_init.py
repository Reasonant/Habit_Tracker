import os
import sqlite3


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
            UNIQUE (date, habit_name),
            FOREIGN KEY (habit_name) REFERENCES habits(name))""")

    db.commit()


def create_database():
    database_name = "main.db"
    current_dir = os.path.dirname(__file__)
    main_dir = os.path.join(os.path.abspath(current_dir), '..', '..')
    path = os.path.join(os.path.abspath(main_dir), database_name)
    db = sqlite3.connect(path)
    create_tables(db)


if __name__ == "__main__":
    create_database()
