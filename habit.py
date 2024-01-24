from db_functions import DBFunctions
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

        :param name: The name of the habit.
        :param periodicity: A timeframe used to track the habit. (For example daily or weekly).
        :param task_specification: The task the user need to perform for this habit. #Decide for this
        """
        self.name = name
        self.periodicity = periodicity
        self.task_specification = task_specification
        self.date_of_creation = str(date.today())
        self.dbf = DBFunctions("main.db")

    def change_periodicity(self, new_periodicity):
        """

        :param new_periodicity: A new value for the timeframe used to track this Habit.
        :return:
        """
        self.dbf.update_habit(self.name, new_periodicity, self.task_specification)

    def change_task_specification(self, new_task_specification):
        self.dbf.update_habit(self.name, self.periodicity, new_task_specification)

    def store(self):
        """
        A function used to store the created habit in the database.
        :return:
        """
        self.dbf.create_habit(self.name, self.periodicity, self.task_specification, self.date_of_creation)

    def complete_task(self, completion_date: str = None):
        """
        A function used to record a task as completed in the database.
        :param completion_date: The datetime the task was completed. It becomes time.today() is not specified.
        :return:
        """
        self.dbf.record_completed_task(self.name, completion_date)
