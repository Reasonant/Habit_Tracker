from src.database.db import update_habit, create_habit, delete_habit, record_completed_task
from datetime import date


class Habits:
    """
    This class implements the concept of a Habit.

    A habit is created when a user wants to track a new habit and record their progress
    or when the program needs to perform some function in the database base on user's instructions.

    :attribute date_of_creation: The date this habit was created as a string in format 'YYYY-MM-DD'.
    :attribute dbf: An instance of the helper class DBFunctions used to perform database operations.

    Methods:
    :method change_periodicity: A method to specify a new period for tracking a habit.
    :method change_task_specification: A method to change the task which corresponds to this Habit.
    :method store: A method to store this habit instance in the database.
    :method complete_task: A method to record the user's progress for this habit.

    """
    def __init__(self, name: str, periodicity: str, task_specification: str):
        """
        The constructor of the Habits class. It creates an instance of the class with the given attributes.

        :param name: The name of the habit.
        :param periodicity: A timeframe used to track the habit. (For example daily or weekly).
        :param task_specification: The task the user need to perform for this habit. (Or a description of the habit)
        """
        self.name = name
        self.periodicity = periodicity.upper()
        self.task_specification = task_specification
        self.date_of_creation = str(date.today())

    def change_periodicity(self, db,  new_periodicity: str):
        """
        A function to change the period this habit is tracked.

        :param db: A sqlite3.Connection object.
        :param new_periodicity: A new value for the timeframe used to track this Habit.
        :return: None
        """
        update_habit(db, self.name, new_periodicity, self.task_specification)

    def change_task_specification(self, db, new_task_specification: str):
        """
        A function to change the task_specification for this habit.

        :param db: A sqlite3.Connection object.
        :param new_task_specification:
        :return: None
        """
        update_habit(db, self.name, self.periodicity, new_task_specification)

    def store(self, db):
        """
        A function used to store the created habit in the database.

        :param db: A sqlite3.Connection object.
        :return: None
        """
        create_habit(db, self.name, self.periodicity, self.task_specification, self.date_of_creation)

    def delete(self, db):
        """
        A function used to delete a habit in the database.

        :param db: A sqlite3.Connection object.
        :return: None
        """
        delete_habit(db, self.name)

    def complete_task(self, db, completion_date: str = None):
        """
        A function used to record a task as completed in the database.

        :param db: A sqlite3.Connection object.
        :param completion_date: The datetime the task was completed. It becomes time.today() is not specified.
        :return: None
        """
        record_completed_task(db, self.name, completion_date)
