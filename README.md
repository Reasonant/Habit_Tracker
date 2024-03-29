# Habit Tracker (Command Line Interface)
## Description

The Habit Tracker is a simple program designed for personal use to help you create, manage and maintain your habits. It runs locally on your device through a Command Line Interface. The project is built using modern python and leverages the built-in libraries that come with it. The main goal of this program is to serve as a minimal self-help tool for everyday use, aiding in personal development. This project is part of an exercise for the course 'Object Oriented and Functional Programming' in the Applied Artificial Intelligence program at IU International University of Applied Sciences.

## Table of contents
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
## Installation

1. Download all the files in a folder on your computer.
    - Click on the 'Code' button in this GitHub Repistory and select 'Download ZIP'.
    - Save the ZIP file to a location on your computer.
    - Locate the downloaded ZIP file and extract its contents.
2. Open a terminal session and navigate to the project folder where you downloaded the files.
    ```bash
    cd path/to/project_folder
    ```

    Replace  'path/to/project_folder' with the actual path to the extracted project folder.

3. Install dependencies using the following command.
      ```bash
      pip install -r requirements.txt
      ```
    This will install the following packages on your computer:
      - [questionary](https://github.com/tmbo/questionary).
      - [pytest](https://docs.pytest.org/en/6.2.x/#).

## Usage

### **Prerequisite** :

Before starting the program you need to create the database if it does not exist.
The database is a file named "main.db" in the top folder. You can create the database by executing the db_init.py. This is for ensuring that the database which the program uses is always of the same type (correct number and names of tables).

You can execute the db_init.py which is located in the src/database folder by moving to the directory where the script is located:
```bash
cd path/to/project_folder/src/database
```
And then typing :
```bash
python db_init.py
```

### The program can be started by typing:
```bash
python main.py
```
1. CREATE A NEW HABIT.

   Here you can create a new habit. You can either choose from predefined habits or create your own. Choosing from predefined asks you to choose a new name for the habit because names are used as identifiers.
For your newly created custom habits you need to specify a name, a tracking period (periodicity) and a task specification (the task you will perform to establish this habit).
2. CHECK-OFF A HABIT.

   Here you can check-off a completed task for a habit. You simply choose the desired habit from the list of tracked habits.

3. MANAGE TRACKED HABITS.

   Here you can either DELETE, CHANGE PERIODICITY or CHANGE TASK_SPECIFICATION for a habit.

4. ANALYSE YOUR HABITS.
   
   Here you can check some statistics for your habits. You can :
   1. View a list of all tracked habits.
   2. View a list of all habits with the same periodicity.
   3. View the current overall streak of all habits.
    4. View the longest streak for a habit (current and lifetime).

## Contributing

**About This Project**

This project is part of my university course in IU International University of Applied Sciences. It's an exercise to understand the concepts of Object Oriented and Functional Programming. Your thoughts and comments will really help me understand these concepts better.

**How You Can Contribute**

- **Suggest Improvements:**  Share ideas on how to make the project better.
- **Report Bugs:**  Please let me know by opening an issue.