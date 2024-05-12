"""
The problem that I wish to solve is a Task Manager. Users will have the ability to create, mark, and remove tasks. In addition, they will be able to see what they have completed and what they will have to complete.

Some of the functions that will be used:
    

Add Task: Users will be asked general questions about the task, including its name, date received, and date due. With this information, the code will append this to a file called “cps109_a1_output.txt”. The code will ensure that the dates are valid and in the correct format (dd/mm/yyyy). However, the code will not check the logic of the date or the user and will not check for leap years. For example, a user could have received a task on 10/11/2023 but the due date was 01/10/2023. 

Remove Task: Users will be asked to specify which task to remove. The code will then search for the task name in the same file used for appending. If it’s found, the task will be removed by storing all the file content into a temporary list, removing the task from the list, and then rewriting the list back to the file (python does not have a .remove() method for file). If the specified task is not found, the code will inform the user of its mistake.

Mark Task: Users will be asked to specify which task to mark as complete. The code for this method will be similar to Remove Task. It will implement the same logic to search for the task by searching through the file. If found, the user will input the date of completion and the code will again implement the same logic to update the file. Same logic if task not found.

Display To Do List: The code will read the file and display tasks that have yet to be finished with their due date. Additionally, it will also display the tasks that have been finished with their completion date.


Notes:

Since Remove Task and Mark Task will share the same logic, there will be a function that updates the file and marks/removes tasks given a parameter job.

There will also be a method to check for the validity of the date

There will be other methods to make the output more user-friendly such as a beginning message, telling the user what option is being performed, and an ending method confirming everything worked. In addition, there will be a loading animation when a function is reading/writing to a file.


"""

# Used for loading animation
from time import sleep


def check(date):
    """
    Checks if date is in dd/mm/yyyy format and is reasonable (42/15/1999 and 1/2a/twenties are invalid).
    Raises ValueError if the conditions are not met.

    :param date: The date to be checked.
    :return: The date if everything is correct, else raises an error.
    """

    # Checks if date can be split into dd/mm/yyyy
    date_format = date.strip(" ").split("/")
    if len(date_format) == 3:

        # Checks if date_format is all integers
        if len([True for i in date_format for j in i if j.isdigit()]) == 8:
            months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

            # Checks if the day, month, and year are valid
            # Checks if dd is in the range of mm and yyyy >= 0
            if int(date_format[-1]) >= 0:
                if 1 <= int(date_format[1]) <= 12:
                    if 1 <= int(date_format[0]) <= months[int(date_format[1]) - 1]:
                        return date

    # Raises ValueError if date format or date values are invalid
    raise ValueError


def top_message(msg):
    """
    Displays a designed message at the top explaining what the code is doing

    :params msg: Message that will be displayed
    :return: None
    """

    print(''.join(["#" for i in range(len(msg))] + ["#" for i in range(12)]))
    print(f"#     {msg}     #")
    print(''.join(["#" for i in range(len(msg))] + ["#" for i in range(12)]) + "\n")


def end_message(msg, func):
    """
    Displays an end message with an optional loading screen

    :param msg: The end message to be displayed
    :param func: Optinal msg to be displayed with loading
    :return: None
    """

    # Displays loading screen if func is not None
    if func != None:
        print(f"\n{func}", end="")

        # Adds a "." every second
        for i in range(4):
            print(".", end="")
            sleep(1)

    # Displays end message
    print(f"\n\n***{msg}***")
    input("\nPress Enter To Continue... ")
    print("\033[H\033[2J", end="")


def add_task(f):
    """
    Adds task to file with details from user input

    :param f: file to be appended to
    :return: None
    """

    top_message("Adding Task")

    # Asks user for name, due date, and date recieved
    task_name = input("Enter Task Name: ")

    # Checks if user enters valid date, else informs user and exits function
    try:
        date_recieved = check(input("Enter Date Task Was Recieved (dd/mm/yyyy): "))
        date_due = check(input("Enter Date Task Due (dd/mm/yyyy): "))

    except ValueError:
        end_message("Invalid Date", None)
        return

    # Appends task and its details to file
    with open(f, "a") as file:
        file.write(f"{task_name}\n")
        file.write("###############################################\n")
        file.write(f"# Date Received (dd/mm/yyyy):    {date_recieved}   #\n")
        file.write("# Date Completed (dd/mm/yyyy):   Unfinished   #\n")
        file.write(f"# Date Due (dd/mm/yyyy):         {date_due}   #\n")
        file.write("###############################################\n\n\n")

    end_message("Task Added Successfully", "Adding")


def update_file(f, job):
    """
    Updates file by removing or marking tasks depending on job

    :param f: file to be updated
    :param job: Marking or Removing
    :return: None
    """

    top_message(f"{job} Task")

    # Asks user for the task to look for
    task_name = input("Enter Task Name: ")
    found = False

    # Reads file and stores its content to info
    with open(f, "r") as file:
        info = file.readlines()

        for i in range(len(info)):

            # Checks to see if task_name is found in info
            if info[i].strip("\n") == task_name:
                found = True

                # If task is found and job is Marking, then it marks it with the date of completion in info
                if job == "Marking":

                    # Checks if user enters valid date, else informs user and exits function
                    try:
                        date_completion = check(input("Enter Date of Completion (dd/mm/yyyy): "))
                    except ValueError:
                        end_message("Invalid Date", None)
                        return

                    # Marks date in info
                    info[i + 3] = f"# Date Completed (dd/mm/yyyy):   {date_completion}   #\n"

                # If task is found and job is not Marking, then removes task from info
                else:
                    del info[i:i + 8]

                # Updates file (writes info on a clear file)
                with open(f, "w") as file1:
                    file1.writelines(info)
                    break

    end_message(f"Task {job[0:-3]}ed Successfully", job) if found else end_message(f'Task "{task_name}" Not Found', "Searching")


def display_list(f, job):
    """
    Displays list of tasks depeneding on job

    :param f: file to be read
    :param job: list of on Unfinished Tasks/Completed Tasks
    :return: None
    """

    top_message(job)
    counter = 1

    # Reads file and stores it in info
    with open(f, "r") as file:
        info = file.readlines()

        # Exits function if file is empty
        if not info:
            end_message("File Empty", None)
            return

        # Gets max length of task name from info (to be used for spacing)
        max_title = max(len(info[i].strip()) for i in range(0, len(info), 8)) + 5

        for i in range(3, len(info), 8):
            task_name = info[i - 3].strip()

            # Prints all unfinished tasks name and thier due date if job = Unfinished Tasks
            if job == "Unfinished Tasks" and "Unfinished" in info[i]:
                print(f"{counter}) {task_name}{((max_title)-len(task_name))*' '}Due: {info[i+1][33:44]}")
                counter += 1

            # Prints all finished tasks name and thier done date if job = Completed Tasks
            elif job == "Completed Tasks" and "Unfinished" not in info[i]:
                print(f"{counter}) {task_name}{((max_title)-len(task_name))*' '}Done: {info[i][33:44]}")
                counter += 1

        end_message("Displayed Successfully", None) if counter > 1 else end_message("Nothing", None)


f = "cps109_a1_output.txt"

# Creates file if not created from before
with open(f, "a") as file:
    pass
user_choice = 0

print("--------------Welcome To Task Manager--------------")
print("    Helping Students Keep Track of Thier Tasks\n\n")

# Options
while user_choice != "5":

    print("""*******************************
*  1) Display Tasks           *
*  2) Add Task                *
*  3) Mark Task               *
*  4) Remove Task             *
*  5) Exit                    *
*******************************""")

    user_choice = input("\nEnter Choice [1-5]: ").strip(" ")
    print("\033[H\033[2J", end="")

    if user_choice == "1":
        display_list(f, "Unfinished Tasks")
        display_list(f, "Completed Tasks")
    elif user_choice == "2":
        add_task(f)
    elif user_choice == "3":
        update_file(f, "Marking")
    elif user_choice == "4":
        update_file(f, "Removing")
    elif user_choice == "5":
        # https://patorjk.com/software/taag/#p=display&f=Graffiti&t=Type%20Something%20%0A
        # https://www.asciiart.eu/computers/smileys
        print("""
          _____                 _   ____             
         / ____|               | | |  _ \\            
        | |  __  ___   ___   __| | | |_) |_   _  ___ 
        | | |_ |/ _ \\ / _ \\ / _` | |  _ <| | | |/ _ \\
        | |__| | (_) | (_) | (_| | | |_) | |_| |  __/
         \\_____|\\___/ \\___/ \\__,_| |____/ \\__, |\\___|
                                          __/ |     
                                         |___/      

                        _.-'''''-._
                      .'  _     _  '.
                     /   (_)   (_)   \\
                    |  ,           ,  | 
                    |  \`.       .`/  |
                     \  '.`'\"'\"'`.'  /
                      '.  `'---'`  .'
                        '-._____.-'
        """)

    # Repeats if user enters anything other than given in the options
    else:
        end_message("Invalid input", None)
