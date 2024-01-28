import questionary
from habit import Habits
from db import create_database, get_all_habits
from analyse import list_all_tracked_habits, list_habits_same_periodicity
from analyse import calculate_streak_one_habit, calculate_overall_streak

# Messages used in questionary calls.
intro_sentence = "Welcome to your Habit Tracking program.\n Shall we proceed ?"
exit_sentence = "See you again !"
main_menu = {'msg': "What would you like to do ?",
             'choices': ["Create a new habit",
                         "Check-off a habit",
                         "Manage tracked habits",
                         "Analyse your habits",
                         "Exit"]}
predefined_choice = {'msg': "", 'choices': ["Choose from predefined", "Create a new habit"]}
analysis_choice = {'msg': "", 'choices': ['Return a list of all currently tracked habits',
                                          'Return a list of all habits with the same periodicity',
                                          'Return the longest run streak of all defined habits',
                                          'Return the longest run streak for a given habit']}
manage_choice = {'msg': "", 'choices': ["Delete a habit",
                                        "Change the periodicity of a habit",
                                        "Change task specification of a habit"]}
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
        streak = calculate_overall_streak(db)
        print(f"The current longest overall streak is: {streak}")
    elif choice == 'Return the longest run streak for a given habit':
        selected_habit = select_habit(db)
        streak = calculate_streak_one_habit(db, selected_habit[0])
        print(f"The current longest streak for this habit is: {streak}")


def cli():
    """
    This function exposes a command line interface for the user to interact with the program.
    It starts a loop and exists when the user chooses : 'Exit' in the main menu.

    :return: None
    """
    db = create_database()

    ans = questionary.confirm(intro_sentence).ask()
    if ans:
        stop = False
    else:
        print(exit_sentence)
        stop = True

    while not stop:
        choice = questionary.select(main_menu['msg'], choices=main_menu['choices']).ask()

        if choice == "Create a new habit":
            handle_new_habit(db)
        elif choice == "Check-off a habit":
            selected_habit = select_habit(db)
            habit = Habits(*selected_habit)
            habit.complete_task(db)
        elif choice == "Manage tracked habits":
            handle_manage_habits(db)
        elif choice == "Analyse your habits":
            handle_analyse_habits(db)
        else:
            print(exit_sentence)
            stop = True


if __name__ == "__main__":
    cli()
