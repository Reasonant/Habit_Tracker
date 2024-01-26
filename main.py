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
manage_choice = {'msg': "", 'choices': ["Delete a habit", "Change the periodicity for a habit",
                                        "Change task specification for a habit"]}
habit_name_choice = "Choose a habit"


def cli():
    """
    This function exposes a command line interface for the user to interact with the program.
    It starts a loop and exists when the user chooses : 'Exit' in the main menu.

    :return: None
    """
    db = create_database()

    def select_habit():
        list_of_habits = get_all_habits(db)
        habits_names = [habit_[0] for habit_ in list_of_habits]
        choice = questionary.select(habit_name_choice, choices=habits_names).ask()
        selected = [habit_ for habit_ in list_of_habits if habit_[0] == choice][0]
        return selected

    ans = questionary.confirm(intro_sentence).ask()
    if ans:
        stop = False
    else:
        print(exit_sentence)
        stop = True

    while not stop:
        choice_1 = questionary.select(main_menu['msg'], choices=main_menu['choices']).ask()

        if choice_1 == "Create a new habit":
            choice_2 = questionary.select(predefined_choice['msg'], choices=predefined_choice['choices']).ask()
            if choice_2 == "Choose from predefined":
                selected_habit = select_habit()
                choice_3 = questionary.text(
                    "Please define a new name for this habit (e.g., 'This_Habits_Name_2'):").ask()
                name, periodicity, task_specification, date_of_creation = selected_habit

                habit = Habits(choice_3, periodicity, task_specification)
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
        elif choice_1 == "Check-off a habit":
            selected_habit = select_habit()
            name, periodicity, task_specification, date_of_creation = selected_habit
            habit = Habits(name, periodicity, task_specification)
            habit.complete_task(db)
            print("Habit checked-off successfully !")
        elif choice_1 == "Manage tracked habits":
            choice_2 = questionary.select(manage_choice['msg'], choices=manage_choice['choices']).ask()
            selected_habit = select_habit()
            name, periodicity, task_specification, date_of_creation = selected_habit
            habit = Habits(name, periodicity, task_specification)
            if choice_2 == "Delete a habit":
                habit.delete(db)
            elif choice_2 == "Change the periodicity for a habit":
                choice_3 = questionary.text("Enter a new periodicity: ").ask()
                habit.change_periodicity(db, choice_3)
            elif choice_2 == "Change task specification for a habit":
                choice_3 = questionary.text("Enter a new task specification: ").ask()
                habit.change_task_specification(db, choice_3)
        elif choice_1 == "Analyse your habits":
            choice_2 = questionary.select(analysis_choice['msg'], choices=analysis_choice['choices']).ask()
            if choice_2 == 'Return a list of all currently tracked habits':
                habits_list = list_all_tracked_habits(db)
                for habit in habits_list:
                    print(habit)
            elif choice_2 == 'Return a list of all habits with the same periodicity':
                periodicity = questionary.select("What is the periodicity ?",
                                                 choices=["DAILY", "WEEKLY"]).ask()
                habits_list = list_habits_same_periodicity(db, periodicity)
                for habit in habits_list:
                    print(habit)
            elif choice_2 == 'Return the longest run streak of all defined habits':
                streak = calculate_overall_streak(db)
                print(f"The longest overall streak is: {streak}")
            elif choice_2 == 'Return the longest run streak for a given habit':
                selected_habit = select_habit()
                streak = calculate_streak_one_habit(db, selected_habit[0])
                print(f"The longest streak for this habit is: {streak}")
        else:
            print(exit_sentence)
            stop = True


if __name__ == "__main__":
    cli()
