import re
import csv
import os
import sys
from datetime import datetime

from entry import Entry


# CSV file name
filename = "worklog.csv"


def clear_screen():
    # Clear screen by sending command to OS.
    os.system('cls' if os.name == 'nt' else 'clear')


class WorkLog(object):
    # All methods for the WorkLog


    def add_new_entry(self, entry):
        # Add a new work log entry.
        self.display_temp_entry(entry)
        while True:
            print("\nWould you like to:\n\n"
                "[S] - Save the entry\n"
                "[E] - Edit the entry\n"
                "[D] - Delete the entry")
            user_input = input("\nPlease select an option: ").lower().strip()
            if user_input == 's':
                self.add_entry_to_file(entry)
                input("\nYour entry has been added! Press ENTER to return to the main menu.")
                self.menu()
            elif user_input == 'e':
                entry = self.edit_entry(entry)
                self.add_new_entry(entry)
            elif user_input == 'd':
                input("\nYour entry has been deleted! Press ENTER to go back to the main menu")
                self.menu()
            else:
                input("\nInvalid entry! See menu for valid options. Press ENTER"
                    " to continue.")


    def display_temp_entry(self, entry):
        # Print task to user before writing to file.
        clear_screen()
        print("Task Name: {}\nTime Spent: {} minutes\nNotes: {}\n"
            "Date: {}".format(entry.task_name,
            entry.time_spent,
            entry.notes,
            entry.date))


    def add_entry_to_file(self, entry):
        # Add entry to CSV file.
        # Check to see if the file already exists
        exists = os.path.isfile(filename)

        with open(filename, 'a') as csvfile:
            fieldnames = ["Task Name", "Time Spent (mins)", "Notes", "Date"]
            entrywriter = csv.DictWriter(csvfile, fieldnames=fieldnames,
             delimiter=',', lineterminator='\n')
            if not exists:
                entrywriter.writeheader()
            entrywriter.writerow({
                fieldnames[0]: entry.task_name,
                fieldnames[1]: entry.time_spent,
                fieldnames[2]: entry.notes,
                fieldnames[3]: entry.date})


    def search_entries(self):
        # Lookup previous entries.
        while True:
            user_input = input("Please choose from the following search options:\n\n"
                "[D] - Search by date\n"
                "[S] - Search by date range\n"
                "[T] - Search by time spent\n"
                "[K] - Search by keyword\n"
                "[R] - Search by regular Expression\n"
                "[Q] - Quit and return to the main menu\n\n"
                ).lower().strip()
            if user_input == 'q':
                self.menu()
            elif user_input == 'd':
                self.search_by_date()
            elif user_input == 's':
                self.search_by_date_range()
            elif user_input == 't':
                self.search_by_time()
            elif user_input == 'k':
                self.search_keyword()
            elif user_input == 'r':
                self.search_regex()
            else:
                clear_screen()
                print("{} is not a valid command! Please try again.\n"
                    "".format(user_input))


    def search_by_date_range(self):
        # Search entries between two dates.
        clear_screen()
        start_date = self.check_date_input("starting")
        end_date = self.check_date_input("ending")

        start_date = datetime.strptime(start_date, "%m/%d/%Y")
        end_date = datetime.strptime(end_date, "%m/%d/%Y")
        clear_screen()

        entries = self.read_csv_file(filename)
        matches = []
        for entry in entries:
            entry_date = datetime.strptime(entry['Date'], "%m/%d/%Y")
            if start_date <= entry_date and end_date >= entry_date:
                matches.append(entry)

        if matches:
            self.display_dates(matches)
        else:
            print("No matches between {} and {}.".format(start_date, end_date))
            input("\Press ENTER to continue")
        clear_screen()
        response = input("Do you want to search something else? Y/[n] ")
        if response.lower() != 'y':
            self.menu()
        else:
            self.search_entries()


    def display_dates(self, matches):
        # Display all the dates that matches between the date range.
        clear_screen()
        dates = self.get_dates_list(matches)
        dates = self.remove_duplicates(dates)
        print("Here are the dates we have entries for: \n")
        for date in dates:
            print(date)
        while True:
            print("\nWould you like to:\n\n"
                "[L] - Look up an entry\n"
                "[S] - Back to the Search Menu\n"
                "[Q] - Back to the Main Menu\n")
            user_input = input("\nSelect one of the options above: ")
            user_input = user_input.lower().strip()
            if user_input == 'l':
                clear_screen()
                self.date_lookup(matches)
            elif user_input == 's':
                clear_screen()
                self.search_entries()
            elif user_input == 'q':
                self.menu()
            else:
                clear_screen()
                print("{} is not a valid command! Please try again.\n"
                    "".format(user_input))


    def date_lookup(self, matches):
        dates = self.get_dates_list(matches)
        dates = self.remove_duplicates(dates)
        print("Here are the dates we have entries for: \n")
        for date in dates:
            print(date)
        user_input = self.validate_date()

        results = []
        for match in matches:
            if user_input == match['Date']:
                results.append(match)
        if results:
            clear_screen()
            self.display_entries(results)
            clear_screen()
        else:
            input("\n{} is not in the search result. Try again."
                "".format(user_input))
            clear_screen()
            self.date_lookup(matches)


    def check_date_input(self, text):
        # For the date range function. Check if input is valid.
        date = input("What is the {} date to search (MM/DD/YYYY): "
            "".format(text))
        try:
            datetime.strptime(date, "%m/%d/%Y")
        except ValueError:
            input("\nNot a valid date entry! Enter the date in the format"
                " MM/DD/YYYY.\n")
            clear_screen()
            return self.check_date_input(text)
        else:
            return date


    def search_by_time(self):
        # Search entries based on time spent.
        matches = []
        clear_screen()
        time = input("Enter time spent to search for: ")
        entries = self.read_csv_file(filename)
        for entry in entries:
            if re.search(r'{}'.format(time), entry['Time Spent (mins)']):
                matches.append(entry)
        if matches:
            self.display_entries(matches)
        else:
            print("No matches found for {} in Time Spent.".format(time))
            input("\nPress ENTER to continue")
        clear_screen()
        response = input("Do you want to search something else? Y/[n] ")
        if response.lower() != 'y':
            self.menu()
        else:
            self.search_entries()


    def search_regex(self):
        # Search through work log using regular expression.
        matches = []
        clear_screen()
        pattern = input("Enter a regular expression: ")
        clear_screen()
        entries = self.read_csv_file(filename)
        for entry in entries:
            if (re.search(r'{}'.format(pattern), entry['Task Name'])
                or re.search(r'{}'.format(pattern), entry['Notes'])):
                matches.append(entry)
        if matches:
            self.display_entries(matches)
        else:
            print("No matches found for {} in Task Name or Notes"
                "".format(pattern))
            input("\nPress ENTER to continue")
        clear_screen()
        response = input("Do you want to search something else? Y/[n] ")
        if response.lower() != 'y':
            self.menu()
        else:
            self.search_entries()


    def search_keyword(self):
        # Search for a keyword (str) that is in either the task name or notes.
        matches = []
        clear_screen()
        user_input = input("Enter a search term: ")
        pattern = "\\b" + user_input + "\\b"
        clear_screen()
        entries = self.read_csv_file(filename)
        for entry in entries:
            if (re.search(r'{}'.format(pattern), entry['Task Name'])
                or re.search(r'{}'.format(pattern), entry['Notes'])):
                matches.append(entry)
        if matches:
            self.display_entries(matches)
        else:
            print("No matches found for {} in Task Name or Notes."
                "".format(user_input))
            input("\nPress ENTER to continue")
        clear_screen()
        response = input("Do you want to search something else? Y/[n] ")
        if response.lower() != 'y':
            self.menu()
        else:
            self.search_entries()


    def remove_duplicates(self, dates):
        # Remove duplicate dates from a list.
        unique_dates = []
        for date in dates:
            if date in unique_dates:
                continue
            else:
                unique_dates.append(date)
        return unique_dates


    def read_csv_file(self, filename):
        # Read a CSV file and return all data in a list.
        import csv
        with open(filename, 'r') as f:
            reader = csv.DictReader(f, delimiter=',', lineterminator='\n')
            rows = list(reader)
        return rows


    def get_dates_list(self, entries):
        # Gets a list of dates for all entries.
        dates = []
        for entry in entries:
            dates.append(entry['Date'])
        return dates


    def search_by_date(self):
        # Find all entries by date.
        clear_screen()
        print("Search by date")
        print('\n' + '=' * 40 + '\n')
        # Find all unique dates and display to user
        entries = self.read_csv_file(filename)
        date_list = self.get_dates_list(entries)
        date_list = self.remove_duplicates(date_list)
        print("Here are the dates we have entries for: \n")
        for date in date_list:
            print(date)
        # Validate date input
        user_input = self.validate_date()
        # Find all and display all entires with the date provided by user
        matches = []
        for line in entries:
            if user_input == line['Date']:
                matches.append(line)
        if matches:
            self.display_entries(matches)
        else:
            print("No matches found for {} in Task Name or Notes."
                "".format(user_input))
            input("\nPress ENTER to continue")
        clear_screen()
        response = input("Do you want to search something else? Y/[n] ")
        if response.lower().strip() != 'y':
            self.menu()
        else:
            clear_screen()
            self.search_entries()


    def print_entries(self, index, entries, display=True):
        # Print entries to screen.
        if display:
            print("Showing {} of {} entry/entries."
                "".format(index + 1, len(entries)))

        print('\n' + '=' * 40 + '\n')
        print("Task Name: {}\nTime Spent: {} minutes\nNotes: {}\n"
            "Date: {}\n".format(
                entries[index]['Task Name'],
                entries[index]['Time Spent (mins)'],
                entries[index]['Notes'],
                entries[index]['Date']))


    def display_nav_options(self, index, entries):
        # Displays a menu that let's the user page through the entries.
        p = "[P] - Previous entry"
        n = "[N] - Next entry"
        q = "[Q] - Return to Main Menu"
        menu = [p, n, q]

        if index == 0:
            menu.remove(p)
        elif index == len(entries) - 1:
            menu.remove(n)

        for option in menu:
            print(option)


    def display_entries(self, entries):
        # Displays entries to the screen.
        index = 0

        while True:
            clear_screen()
            self.print_entries(index, entries)

            if len(entries) == 1:
                input("\nPress ENTER to continue to the main menu.")
                self.menu()

            self.display_nav_options(index, entries)

            user_input = input("\nSelect option from above: ").lower().strip()

            if index == 0 and user_input == 'n':
                index += 1
                clear_screen()
            elif index > 0 and index < len(entries) - 1 and user_input == 'n':
                index += 1
                clear_screen()
            elif index == len(entries) - 1 and user_input == 'p':
                index -= 1
                clear_screen()
            elif user_input == 'q':
                self.menu()
            else:
                input("\n{} is not a valid command! Please try again."
                    "".format(user_input))


    def validate_date(self):
        # Validate date input.
        date = input("\nPlease enter the date of the task in the format MM/DD/YYYY: ")
        try:
            datetime.strptime(date, "%m/%d/%Y")
        except ValueError:
            input("\nNot a valid date entry! Enter the date in the format"
                " MM/DD/YYYY.\n")
            self.validate_date()
        else:
            return date


    def edit_entry(self, entry):
        # Edits an entry either by Task Name, Time Spent, Notes, or Date.
        clear_screen()
        while True:
            print("Would you like to update the following\n\n"
                "[N] - Task name\n"
                "[T] - Task time\n"
                "[S] - Task notes\n"
                "[D] - Task date\n")
            user_input = input("Your choice from above: ").lower().strip()
            if user_input == 'n':
                entry.get_task_name()
                input("\nTask name edited. Press ENTER to continue.")
                self.add_new_entry(entry)
            elif user_input == 't':
                entry.get_time_spent()
                input("\nTime spent edited. Press ENTER to continue.")
                self.add_new_entry(entry)
            elif user_input == 's':
                entry.get_notes()
                input("\nNotes edited. Press ENTER to continue.")
                self.add_new_entry(entry)
            elif user_input == 'd':
                entry.get_date()
                input("\nDate edited. Press ENTER to continue.")
                self.add_new_entry(entry)
            else:
                clear_screen()
                print("{} is not a valid command! Please try again.\n"
                    "".format(user_input))


    def menu(self):
        # Present menu to user.
        clear_screen()
        print("Welcome to Work Log 3.0!\n")
        while True:
            user_input = input(
                "Please choose from the following options:\n\n"
                "[A] - Add new work entry\n"
                "[S] - Search work entries\n"
                "[Q] - Quit Work Log 3.0\n\n"
            )
            if user_input.lower().strip() == 'q':
                print("Thanks for using Work Log 3.0!")
                sys.exit()
            elif user_input.lower().strip() == 'a':
                clear_screen()
                entry = Entry()
                self.add_new_entry(entry)
            elif user_input.lower().strip() == 's':
                clear_screen()
                self.search_entries()
            else:
                clear_screen()
                print("{} is not a valid command! Please try again.\n"
                    "".format(user_input))


    def __init__(self):
        super(WorkLog, self).__init__()
        self.menu()


if __name__ == "__main__":
    WorkLog() 