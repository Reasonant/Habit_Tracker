import sqlite3
import questionary
from src.habit import Habits
from utils.utils import handle_new_habit, handle_manage_habits, handle_analyse_habits, select_habit
from src.database.db import insert_initial_data
import os

# Message used in questionary call.
main_menu = {'msg': "What would you like to do ?",
             'choices': ["Create a new habit",
                         "Check-off a habit",
                         "Manage tracked habits",
                         "Analyse your habits",
                         "Exit"]}


def cli():
    """
    This function exposes a command line interface for the user to interact with the program.
    It starts a loop and exits when the user chooses : 'Exit' in the main menu.

    :return: None
    """
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.db")

    if os.path.exists(path):

        db = sqlite3.connect("main.db")
        insert_initial_data(db)

        questionary.print("\nWelcome to your Habit Tracking program.")
        questionary.print("This program lets you define and manage your habits.\n", style="italic")
        stop = False
    else:
        stop = True
        print("The database does not exist. Please create it using the 'db_init.py' module.")

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
            print("See you again !")
            stop = True


if __name__ == "__main__":
    cli()
