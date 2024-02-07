from habit import Habits
from db import get_all_habits, update_habit
from db import create_database, create_habit, get_habit
from db import delete_habit, record_completed_task
from db import get_habit_records_by_name, get_all_habits_records, get_habits_by_periodicity

from analyse import list_all_tracked_habits, list_habits_same_periodicity
from analyse import calculate_streak_one_habit, calculate_overall_streak, calculate_longest_lifetime_streak

from datetime import date, timedelta


class TestHabit:

    def setup_method(self):
        self.db = create_database("test.db")

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

        strk_1 = calculate_streak_one_habit(self.db, test_habit.name)

        strk_2 = calculate_longest_lifetime_streak(self.db, test_habit.name)

        s = get_habit_records_by_name(self.db, test_habit.name)

        assert strk_1 == 3
        assert strk_2 == 4


    def teardown_method(self):
        self.db.close()
        import os
        os.remove("test.db")
