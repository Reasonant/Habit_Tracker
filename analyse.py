from db import get_all_habits, get_habits_by_periodicity
from db import get_habit_records_by_name, get_all_habits_records, get_habit
from datetime import datetime, timedelta


def calculate_streak_daily(dates_list: list[datetime]) -> int:
    """
    Helper function to calculate current daily streak from stored records of completed tasks for a habit.

    :param dates_list: A list of datetime objects
    :return: The current streak
    """

    if not dates_list:
        return 0

    dates_list.sort(reverse=True)

    streak = 1 if datetime.now().date() == dates_list[0].date() else 0
    ref = datetime.now() - timedelta(days=1)
    for date in dates_list[streak:]:
        if date.date() == ref.date():
            streak += 1
            ref -= timedelta(days=1)
        else:
            break
    return streak


def calculate_streak_weekly(dates_list: list[datetime]) -> int:
    """
    Helper function to calculate current weekly streak from stored records of completed tasks for a habit.
    :param dates_list: A list of datetime objects.
    :return: The current streak.
    """

    if not dates_list:
        return 0

    dates_list.sort(reverse=True)

    weeks = [w.isocalendar()[1] for w in dates_list]
    temp = []
    temp = [w for w in weeks if w not in temp]
    weeks = temp
    this_week = datetime.now().isocalendar()[1]
    streak = []
    if len(weeks) == 1:
        if weeks[0] == this_week:
            streak.append(1)
            return sum(streak)
    elif len(weeks) >= 2 and weeks[0] == this_week:
        streak.append(1)
        for w in range(0, len(weeks) - 1):
            diff = weeks[w] - weeks[w + 1]
            if diff == 1:
                streak.append(1)
            else:
                break
        return sum(streak)
    else:
        return 0


def list_all_tracked_habits(db) -> list[str]:
    """
    Function to return a list of all tracked habits in the database.

    :param db: A sqlite3.Connection object.
    :return: A list of strings : The data of the habits stored in the database
    """
    habits_list = get_all_habits(db)
    habits_list = [f"{i}." + " " + t[0] + f" ({t[1]})" + f" ({t[2]})" for i, t in enumerate(habits_list, start=1)]
    return habits_list


def list_habits_same_periodicity(db, periodicity: str) -> list[str]:
    """
    Function to return a list of all habits with the same periodicity, stored in the database.

    :param db: A sqlite3.Connection object.
    :param periodicity: A desired string value between DAILY and WEEKLY to determine fetched habits.
    :return: A list of strings : The data of the habits with the periodicity specified above.
    """
    habits_list = get_habits_by_periodicity(db, periodicity)
    habits_list = [f"{i}." + " " + t[0] + f" ({t[1]})" + f" ({t[2]})" for i, t in enumerate(habits_list, start=1)]
    return habits_list


def calculate_streak_one_habit(db, habit_name: str) -> int:
    """
    Function to calculate the longest streak of a habit with the given name as input.

    :param db: A sqlite3.Connection object.
    :param habit_name: The name of the habit which streaks will be calculated.
    :return: An integer representing the current streak.
    """
    habit_records = get_habit_records_by_name(db, habit_name)
    periodicity = get_habit(db, habit_name)[1]
    dates = [record[0] for record in habit_records]
    dates = [datetime.strptime(date_str, "%Y-%m-%d") for date_str in dates]
    if periodicity == "DAILY":
        streak = calculate_streak_daily(dates)
    elif periodicity == "WEEKLY":
        streak = calculate_streak_weekly(dates)
    else:
        return 0

    return streak


def calculate_overall_streak(db) -> int:
    """
    Function to calculate the longest overall streak of all habits' records stored in the database.

    :param db: A sqlite3.Connection object.
    :return: The maximum current streak among all habits' records.
    """
    habits = get_all_habits(db)
    streaks = []
    for habit in habits:
        streak = calculate_streak_one_habit(db, habit[0])
        streaks.append(streak)
    return max(streaks)
