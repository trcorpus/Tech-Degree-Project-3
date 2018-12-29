from datetime import datetime


class Entry(object):
    # Docstring for Entry
    def __init__(self):
        super(Entry, self).__init__()
        self.get_task_name()
        self.get_time_spent()
        self.get_notes()
        self.get_date()


    def get_task_name(self):
        # Ask user to enter their task name.
        task_name = input("Enter a task name: ")
        if len(task_name) == 0:
            input("\nTask name cannot be empty!\n")
            self.get_task_name()
        else:
            self.task_name = task_name


    def get_time_spent(self):
        # Ask user to enter the time spent on the task. Check if the input is
        # valid.
        minutes = input("Enter number of minutes spent working on the task: ")
        try:
            int(minutes)
        except ValueError:
            input("\nNot a valid time entry! Enter time as a whole integer,"
            " i.e. 45.\n")
            self.get_time_spent()
        else:
            self.time_spent = minutes


    def get_notes(self):
        # Ask user to enter any additional notes for the task.
        notes = input("Notes for this task (Enter if None): ")
        self.notes = notes


    def get_date(self):
        # Ask user for date in the format of mm/dd/yyyy. Check if valid entry.
        date = input("Enter date of task in the format MM/DD/YYY: ")
        try:
            datetime.strptime(date, "%m/%d/%Y")
        except ValueError:
            input("\nNot a valid date entry! Enter the date in the format"
            " MM/DD/YYYY.\n")
            self.get_date()
        else:
            self.date = date


    def __str__(self):
        return """Task Name: {}
        Date Recorded: {}
        Time Spent: {} minutes
        Notes: {}
        """.format(self.task_name,
                self.date,
                self.time_spent,
                self.notes
                )