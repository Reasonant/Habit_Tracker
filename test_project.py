from habit import Habits
from db import DB, DBFunctions
from analyse import list_all_tracked_habits, list_habits_same_periodicity
from analyse import calculate_streak_one_habit, calculate_overall_streak


class TestHabit:

    def setup_method(self):
        self.test_habits = [("Running", "Daily", "2024-01-18"),
                       ("Reading", "Weekly", "2024-01-19"),
                       ("Swimming", "Daily", "2024-01-20"),
                       ("Meditation", "Daily", "2024-01-21"),
                       ("Gardening", "Monthly", "2024-01-22"),
                       ("Coding", "Daily", "2024-01-23"),
                       ("Walking", "Weekly", "2024-01-24"),
                       ("Yoga", "Daily", "2024-01-25"),
                       ("Writing", "Daily", "2024-01-26"),
                       ("Cooking", "Weekly", "2024-01-27")]
        self.db = DB("test.db")
        self.dbf = DBFunctions("test.db")
        self.dbf.create_habit("test_habit_1", "test_periodicity_1",
                              "test_task_specification_1", "2024-01-16")

    def test_habit(self):
        habit = Habits("test_habit_1", "test_periodicity_1",
                       "test_task_specification_1")
        habit.store()
        habit.complete_task()

    def test_db(self):
        for _ in range(5):
            n, p, d = self.test_habits[_]
            self.dbf.update_habit(n, p, d)
            print(f"Updated habit {n} successfully !")
        n = "Swimming"
        self.dbf.delete_habit(n)
        print(f"Deleted habit {n} successfully !")
        n = "Meditation"
        self.dbf.record_completed_task(n)
        print(f"Recorded progress for habit {n}.")
        n = "Reading"
        self.dbf.record_completed_task(n)
        print(f"Recorded progress for habit {n}.")
        habits_list = self.dbf.get_all_habits()
        print(f"These are the tracked habits: {habits_list}")
        n = "Writing"
        records = self.dbf.get_habit_records_by_name(n)
        print(f"Records for habit {n} : {records}")
        n = "Swimming"
        records = self.dbf.get_habit_records_by_name(n)
        print(f"Records for habit {n} : {records}")
        n = "Reading"
        records = self.dbf.get_habit_records_by_name(n)
        print(f"Records for habit {n} : {records}")
        habits_list = self.dbf.get_all_habits_records()
        print(f"These are the current records : {habits_list}")
        p = "Daily"
        habits_list = self.dbf.get_habits_by_periodicity(p)
        print(f"These are the habits of periodicity {p}: {habits_list}")

    def teardown_method(self):
        pass
        """
        self.dbf.close_connection()
        import os
        os.remove("test.db")
        """
