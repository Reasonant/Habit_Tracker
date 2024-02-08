import questionary
from src.database.db import get_all_habits
from src.habit import Habits
from src.analyse import list_all_tracked_habits, list_habits_same_periodicity, calculate_overall_streak
from src.analyse import calculate_streak_one_habit, calculate_longest_lifetime_streak

# Messages used in questionary calls.
predefined_choice = {'msg': "", 'choices': ["Choose from predefined", "Create a new habit"]}
manage_choice = {'msg': "", 'choices': ["Delete a habit",
                                        "Change the periodicity of a habit",
                                        "Change task specification of a habit"]}
analysis_choice = {'msg': "", 'choices': ['Return a list of all currently tracked habits',
                                          'Return a list of all habits with the same periodicity',
                                          'Return the longest run streak of all defined habits',
                                          'Return the longest run streak for a given habit']}
habit_name_choice = "Choose a habit"


def select_habit(db) -> tuple:
    """
    This function is used to print available choices to the user through questionary.
    :param db: A sqlite3.Connection object.
    :return: The selected habit as a tuple. (NAME, PERIODICITY, TASK_SPECIFICATION)
    """
    list_of_habits = get_all_habits(db)
    choices = [f"{i}. {t[0]} ({t[1]}) ({t[2]})" for i, t in enumerate(list_of_habits, start=1)]
    choice = questionary.select(habit_name_choice, choices=choices).ask()
    selected = list_of_habits[int(choice[0]) - 1]
    selected = selected[:-1]
    return selected


def handle_new_habit(db):
    """
    This function handles the habit creation submenu in the main U.I.
    It asks the user to choose from Predefined Habits or to create a new habit.
    Then it executes the creation of the habit.

    :param db: The database connection object.
    :return: None
    """
    choice = questionary.select(predefined_choice['msg'], choices=predefined_choice['choices']).ask()
    if choice == "Choose from predefined":
        selected_habit = list(select_habit(db))
        choice_3 = questionary.text(
            "Please define a new name for this habit (e.g., 'This_Habits_Name_2'):").ask()
        selected_habit[0] = choice_3
        habit = Habits(*selected_habit)
        habit.store(db)
        print("Habit created successfully !")
    else:
        name = questionary.text("What is the name of the habit you want to create ?").ask()
        periodicity = questionary.select(
            "What is the periodicity of the new habit ?", choices=["DAILY", "WEEKLY"]).ask()
        task_specification = questionary.text(
            "What is the task specification of the new habit ?").ask()

        habit = Habits(name, periodicity, task_specification)
        habit.store(db)
        print("Habit created successfully !")


def handle_manage_habits(db):
    """
    This function handles the habit management submenu.
    Available choices are: Habit Deletion, Change tracking timeframe (periodicity), Change task specification.

    :param db: The database connection object.
    :return: None
    """
    choice = questionary.select(manage_choice['msg'], choices=manage_choice['choices']).ask()
    selected_habit = select_habit(db)
    habit = Habits(*selected_habit)
    if choice == "Delete a habit":
        habit.delete(db)
    elif choice == "Change the periodicity of a habit":
        choice= questionary.select("Select a new periodicity: ", choices=["DAILY", "WEEKLY"]).ask()
        habit.change_periodicity(db, choice)
    elif choice == "Change task specification of a habit":
        choice = questionary.text("Enter a new task specification: ").ask()
        habit.change_task_specification(db, choice)


def handle_analyse_habits(db):
    """
    This function handles the habits analysis submenu.

    :param db: The database connection object.
    :return:
    """
    choice = questionary.select(analysis_choice['msg'], choices=analysis_choice['choices']).ask()
    if choice == 'Return a list of all currently tracked habits':
        habits_list = list_all_tracked_habits(db)
        for habit in habits_list:
            print(habit)
    elif choice == 'Return a list of all habits with the same periodicity':
        periodicity = questionary.select("What is the periodicity ?",
                                         choices=["DAILY", "WEEKLY"]).ask()
        habits_list = list_habits_same_periodicity(db, periodicity)
        if habits_list:
            for habit in habits_list:
                print(habit)
        else:
            print(f"There are no habits with {periodicity} periodicity currently recorded.")
    elif choice == 'Return the longest run streak of all defined habits':
        streak_weekly, streak_daily = calculate_overall_streak(db)
        print(f"The current longest overall streak (for weekly habits) is: {streak_weekly}")
        print(f"The current longest overall streak (for daily habits) is: {streak_daily}")
    elif choice == 'Return the longest run streak for a given habit':
        selected_habit = select_habit(db)
        streak = calculate_streak_one_habit(db, selected_habit[0])
        lifetime_streak = calculate_longest_lifetime_streak(db, selected_habit[0])
        print(f"The current longest streak for this habit is: {streak}")
        print(f"The longest lifetime streak for this habit is: {lifetime_streak}")
