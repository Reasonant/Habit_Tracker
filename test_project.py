from habit import Habits
from db import get_all_habits, update_habit
from db import create_database, create_habit, get_habit
from db import delete_habit, record_completed_task
from db import get_habit_records_by_name, get_all_habits_records, get_habits_by_periodicity

from analyse import list_all_tracked_habits, list_habits_same_periodicity
from analyse import calculate_streak_one_habit, calculate_overall_streak


class TestHabit:

    def setup_method(self):
        self.test_habits = [("Running", "DAILY", "To run", "2024-01-18"),
                            ("Reading", "WEEKLY", "To read", "2024-01-19"),
                            ("Swimming", "DAILY", "To swim",  "2024-01-20"),
                            ("Meditation", "DAILY", "To meditate", "2024-01-21"),
                            ("Gardening", "WEEKLY", "Water flowers", "2024-01-22"),
                            ("Coding", "DAILY", "Write a program", "2024-01-23"),
                            ("Walking", "WEEKLY", "Walk a mile", "2024-01-24"),
                            ("Yoga", "DAILY", "Sit and listen", "2024-01-25"),
                            ("Writing", "DAILY", "Write a page",  "2024-01-26"),
                            ("Cooking", "WEEKLY", "Make a food",  "2024-01-27")]
        self.db = create_database("test.db")

        for _ in self.test_habits:
            create_habit(self.db, *_)
        test_dates = ["2022-05-18", "2023-03-22", "2024-06-05", "2021-02-15", "2025-07-12", "2022-04-10",
                      "2023-08-23", "2024-01-08", "2022-11-20", "2023-09-14", "2024-12-03", "2021-10-01"]
        n = "Cooking"
        for d in test_dates:
            record_completed_task(self.db, n, d)
        test_dates = ["2023-08-23", "2023-08-24", "2024-06-05", "2021-02-15", "2025-07-12",
                      "2022-04-10", "2023-01-08", "2022-12-03", "2024-10-01", "2022-05-18",
                      "2023-08-25", "2024-01-01", "2025-03-22"]
        n = "Writing"
        for d in test_dates:
            record_completed_task(self.db, n, d)

    def test_habit(self):
        print("HABIT.py TEST\n\n")
        habit = Habits("test_habit_1", "test_periodicity_1",
                       "test_task_specification_1")
        habit.store(self.db)
        habit.complete_task(self.db)
        print("HABIT.py TEST OVER\n\n")

    def test_db(self):
        print("DB.py TEST\n\n")
        for _ in self.test_habits:
            create_habit(self.db, *_)
        test_dates = ["2022-05-18", "2023-03-22", "2024-06-05", "2021-02-15", "2025-07-12", "2022-04-10",
                      "2023-08-23", "2024-01-08", "2022-11-20", "2023-09-14", "2024-12-03", "2021-10-01"]
        n = "Cooking"
        for d in test_dates:
            record_completed_task(self.db, n, d)
        test_dates = ["2023-08-23", "2022-11-20", "2024-06-05", "2021-02-15", "2025-07-12",
                      "2022-04-10", "2023-01-08", "2022-12-03", "2024-10-01", "2022-05-18",
                      "2023-09-14", "2024-01-01", "2025-03-22"]
        n = "Writing"
        for d in test_dates:
            record_completed_task(self.db, n, d)
        test_dates = ["2023-02-15", "2024-07-05", "2021-12-20", "2023-10-15", "2022-08-05",
                      "2024-05-01", "2025-01-15", "2022-04-20", "2023-11-30", "2024-06-25",
                      "2022-02-01", "2025-08-10", "2023-03-20", "2024-09-05", "2021-11-10",
                      "2023-06-01", "2022-12-15", "2024-03-10", "2025-05-25", "2022-07-10"]
        n = "Yoga"
        for d in test_dates:
            record_completed_task(self.db, n, d)

        n = "Swimming"
        delete_habit(self.db, n)
        print(f"Deleted habit {n} successfully !")

        n = "Swimming"
        p = "WEEKLY"
        t = "To swim"
        update_habit(self.db, n, p, t)

        n = "Meditation"
        record_completed_task(self.db, n)
        print(f"Recorded progress for habit {n}.")

        n = "Reading"
        record_completed_task(self.db, n)
        print(f"Recorded progress for habit {n}.")

        habits_list = get_all_habits(self.db)
        print(f"These are the tracked habits: {habits_list}")

        n = "Writing"
        records = get_habit_records_by_name(self.db, n)
        print(f"Records for habit {n} : {records}")

        n = "Swimming"
        records = get_habit_records_by_name(self.db, n)
        print(f"Records for habit {n} : {records}")

        n = "Reading"
        records = get_habit_records_by_name(self.db, n)
        print(f"Records for habit {n} : {records}")

        habits_list = get_all_habits_records(self.db)
        print(f"These are the current records : {habits_list}")

        p = "DAILY"
        habits_list = get_habits_by_periodicity(self.db, p)
        print(f"These are the habits of periodicity {p}: {habits_list}")

        n = "Swimming"
        get_habit(self.db, n)

        print("DB.py TEST OVER\n\n")

    def test_analyse(self):
        print("ANALYSE.py TEST\n\n")
        n = 'Writing'
        h = get_habit_records_by_name(self.db, n)
        print(h)
        print()

        l = list_all_tracked_habits(self.db)
        print(f"List of tracked habits {l}")

        p = "DAILY"
        l = list_habits_same_periodicity(self.db, p)
        print(f"List of DAILY habits {l}")

        n = "Writing"
        s = calculate_streak_one_habit(self.db, n)
        print(f"Streak of {n} is {s}")

        n = "Writing"
        s = calculate_streak_one_habit(self.db, n)
        print(f"Streak of {n} is {s}")
        print("ANALYSE.py TEST OVER\n\n")

    def teardown_method(self):
        self.db.close()
        import os
        os.remove("test.db")
