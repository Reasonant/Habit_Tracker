from db_functions import DBFunctions
from datetime import datetime, timedelta

dbf = DBFunctions("main.db")


def calculate_streaks(dates_list: list):
    """
    Helper function to calculate streaks from stored records of completed tasks for a Habit

    :param dates_list: a list of datetime objects
    :return: a list of streaks
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


def list_all_tracked_habits():
    habits_list = list(dbf.get_all_habits())
    habits_list = [habit[0] for habit in habits_list]
    return habits_list


def list_habits_same_periodicity(periodicity):
    habits_list = list(dbf.get_habits_by_periodicity(periodicity))
    habits_list = [habit[0] for habit in habits_list]
    return habits_list


def calculate_streak_one_habit(habit_name):
    habit_records = dbf.get_habit_records_by_name(habit_name)
    dates = [habit[0] for habit in habit_records]

    dates = [datetime.strptime(date_str, "%Y-%m-%d") for date_str in dates]
    streaks = calculate_streaks(dates)
    return max(streaks)


def calculate_overall_streak():
    habits = list_all_tracked_habits()
    streaks = []
    for habit in habits:
        streak = calculate_streak_one_habit(habit)
        streaks.append(streak)
    return max(streaks)
