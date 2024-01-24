import questionary
from habit import Habits
from db import create_database
from db_functions import DBFunctions
from analyse import list_all_tracked_habits, list_habits_same_periodicity
from analyse import calculate_streak_one_habit, calculate_overall_streak

intro_sentence = "Welcome to your Habit Tracking program.\n Shall we proceed ?"
exit_sentence = "See you again !"
main_menu = {'msg': "What would you like to do ?",
             'choices': ["Create a new habit",
                         "Check-off a habit",
                         "Analyse your habits",
                         "Exit"]}
predefined_choice = {'msg': " ", 'choices': ["Choose from predefined", "Create a new habit"]}
analysis_choice = {'msg': " ", 'choices': ['Return a list of all currently tracked habits',
                                           'Return a list of all habits with the same periodicity',
                                           'Return the longest run streak of all defined habits',
                                           'Return the longest run streak for a given habit']}


def cli():
    create_database()
    dbf = DBFunctions("main.db")

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
                habits_list = dbf.get_all_habits()
                habits_names = [habit[0] for habit in habits_list]
                choice_3 = questionary.select("", choices=habits_names).ask()
                selected_habit = [habit for habit in habits_list if habit[0] == choice_3]
                print(selected_habit)
                name, periodicity, task_specification, date_of_creation = selected_habit[0]

                habit = Habits(name, periodicity, task_specification)
                habit.store()
                print("Habit created successfully !")
            else:
                name = questionary.text(
                    "What is the name of the habit you want to create ?"
                ).ask()
                periodicity = questionary.select(
                    "What is the periodicity of the new habit ?",
                    choices=["Daily", "Weekly"]
                ).ask()
                task_specification = questionary.text(
                    "What is the task specification of the new habit ?"
                ).ask()

                habit = Habits(name, periodicity, task_specification)
                habit.store()
                print("Habit created successfully !")
        elif choice_1 == "Check-off a habit":
            print("Which habit's task do you want to mark as completed ?")
            habits_list = dbf.get_all_habits()
            habits_names = [habit[0] for habit in habits_list]
            choice_2 = questionary.select("", choices=habits_names).ask()
            selected_habit = [habit for habit in habits_list if habit[0] == choice_2]
            name, periodicity, task_specification, date_of_creation = selected_habit[0]
            habit = Habits(name, periodicity, task_specification)
            habit.complete_task()
            print("Habit checked-off successfully !")
        elif choice_1 == "Analyse your habits":
            choice_2 = questionary.select(analysis_choice['msg'], choices=analysis_choice['choices']).ask()
            if choice_2 == 'Return a list of all currently tracked habits':
                habits_list = list_all_tracked_habits()
                for habit in habits_list:
                    print(habit)
            elif choice_2 == 'Return a list of all habits with the same periodicity':
                periodicity = questionary.select("What is the periodicity ?",
                                                 choices=["Daily", "Weekly"]).ask()
                habits_list = list_habits_same_periodicity(periodicity)
                for habit in habits_list:
                    print(habit)
            elif choice_2 == 'Return the longest run streak of all defined habits':
                streak = calculate_overall_streak()
                print(f"The longest overall streak is: {streak}")
            elif choice_2 == 'Return the longest run streak for a given habit':
                name = questionary.text("What is the name of the habit ?").ask()
                streak = calculate_streak_one_habit(name)
                print(f"The longest streak for this habit is: {streak}")
        else:
            print(exit_sentence)
            stop = True


if __name__ == "__main__":
    cli()
