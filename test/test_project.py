import sqlite3
from datetime import date, timedelta

from src.analyse import calculate_streak_one_habit, calculate_longest_lifetime_streak
from src.database.db import record_completed_task, insert_initial_data
from src.database.db_init import create_tables
from src.habit import Habits


class TestHabit:

    def setup_method(self):
        self.db = sqlite3.connect("test.db")
        create_tables(self.db)
        insert_initial_data(self.db)

    def test_habits(self):
        """
        Tests habit creation and functionality.
        :return:
        """
        test_habit = Habits("Test_habit_1", "DAILY", "Test this habit")
        test_habit.store(self.db)
        test_habit.change_periodicity(self.db, "WEEKLY")
        test_habit.change_task_specification(self.db, "Test this new specification")

    def test_recording_a_habit(self):
        test_habit = Habits("Test_habit_1", "DAILY", "Test this habit")
        test_habit.store(self.db)

        record_completed_task(self.db, test_habit.name)
        record_completed_task(self.db, test_habit.name, str(date.today() - timedelta(days=1)))
        record_completed_task(self.db, test_habit.name, str(date.today() - timedelta(days=2)))

        record_completed_task(self.db, test_habit.name, str(date.today() - timedelta(days=4)))
        record_completed_task(self.db, test_habit.name, str(date.today() - timedelta(days=5)))
        record_completed_task(self.db, test_habit.name, str(date.today() - timedelta(days=6)))
        record_completed_task(self.db, test_habit.name, str(date.today() - timedelta(days=7)))

        streak_current = calculate_streak_one_habit(self.db, test_habit.name)

        streak_lifetime = calculate_longest_lifetime_streak(self.db, test_habit.name)

        assert streak_current == 3
        assert streak_lifetime == 4

    def teardown_method(self):
        self.db.close()
        import os
        os.remove("test.db")
