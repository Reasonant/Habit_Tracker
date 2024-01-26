from db import get_all_habits, get_habits_by_periodicity, get_habit_records_by_name, get_all_habits_records
from datetime import datetime, timedelta


def calculate_streaks(dates_list: list[datetime]) -> list[int]:
    """
    Helper function to calculate streaks from stored records of completed tasks for a Habit.

    :param dates_list: A list of datetime objects
    :return: A list of integers (streaks)
    """
    streaks = []
    current_streak = 0
    dates_list.sort()
    for i in range(len(dates_list) - 1):
        if dates_list[i] + timedelta(days=1) == dates_list[i + 1]:
            current_streak += 1
        else:
            if current_streak > 0:
                streaks.append(current_streak + 1)
            current_streak = 0
    if current_streak > 0:
        streaks.append(current_streak + 1)
    return streaks


def list_all_tracked_habits(db) -> list[str]:
    """
    Function to return a list of all tracked habits in the database.

    :param db: A sqlite3.Connection object.
    :return: A list of strings : The names of the habits stored in the database
    """
    habits_list = list(get_all_habits(db))
    habits_list = [habit[0] for habit in habits_list]
    return habits_list


def list_habits_same_periodicity(db, periodicity: str) -> list[str]:
    """
    Function to return a list of all habits with the same periodicity, stored in the database.

    :param db: A sqlite3.Connection object.
    :param periodicity: A desired string value between DAILY and WEEKLY to determine fetched habits.
    :return: A list of strings : The names of the habits with the periodicity specified above.
    """
    habits_list = list(get_habits_by_periodicity(db, periodicity))
    habits_list = [habit[0] for habit in habits_list]
    return habits_list


def calculate_streak_one_habit(db, habit_name: str) -> int:
    """
    Function to calculate the longest streak of a habit with the given name as input.

    :param db: A sqlite3.Connection object.
    :param habit_name: The name of the habit which streaks will be calculated.
    :return: An integer representing the maximum streak (in days).
    """
    habit_records = get_habit_records_by_name(db, habit_name)
    dates = [habit[0] for habit in habit_records]

    dates = [datetime.strptime(date_str, "%Y-%m-%d") for date_str in dates]
    streaks = calculate_streaks(dates)
    if streaks:
        return max(streaks)
    else:
        return 0


def calculate_overall_streak(db) -> int:
    """
    Function to calculate the longest overall streak of all habits' records stored in the database.

    :param db: A sqlite3.Connection object.
    :return: None
    """
    habits = get_all_habits_records(db)
    habits = [habit[1] for habit in habits]
    streaks = []
    for habit in habits:
        streak = calculate_streak_one_habit(habit)
        streaks.append(streak)
    return max(streaks)
