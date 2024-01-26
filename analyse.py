from db import get_all_habits, get_habits_by_periodicity
from db import get_habit_records_by_name, get_all_habits_records, get_habit
from datetime import datetime, timedelta, date


def calculate_streak(dates_list: list[datetime], timeframe: str) -> int:
    """
    Helper function to calculate streaks from stored records of completed tasks for a Habit.

    :param dates_list: A list of datetime objects
    :param timeframe: The timeframe to check for streaks. (DAILY or WEEKLY)
    :return: The current streak
    """
    dates_list.sort(reverse=True)

    if timeframe == "DAILY":
        streak = 0
        for i in range(len(dates_list) - 1):
            if dates_list[i] - timedelta(days=1) == dates_list[i + 1]:
                streak += 1
            else:
                streak = 0
        if streak > 0:
            streak += 1
        return streak
    elif timeframe == "WEEKLY":
        weekdays = []
        for weekday in dates_list:
            weekdays.append(int(weekday.strftime("%U")))

        streak = 0
        for i in range(len(weekdays) - 1):
            if weekdays[i] + 1 == weekdays[i + 1]:
                streak += 1
            else:
                streak = 0
        if streak > 0:
            streak += 1
        return streak


def list_all_tracked_habits(db) -> list[str]:
    """
    Function to return a list of all tracked habits in the database.

    :param db: A sqlite3.Connection object.
    :return: A list of strings : The names of the habits stored in the database
    """
    habits_list = get_all_habits(db)
    habits_list = [f"{i}." + " " + t[0] + f" ({t[1]})" + f" ({t[2]})" for i, t in enumerate(habits_list, start=1)]
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
    :return: A list of integers representing the maximum streaks (in days).
    """
    habit_records = get_habit_records_by_name(db, habit_name)
    periodicity = get_habit(db, habit_name)[1]
    dates = [habit[0] for habit in habit_records]
    dates = [datetime.strptime(date_str, "%Y-%m-%d") for date_str in dates]
    streak = calculate_streak(dates, periodicity)

    return streak


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
        streak = calculate_streak_one_habit(db, habit)
        streaks.append(streak)
    return max(streaks)
