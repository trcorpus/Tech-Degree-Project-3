import csv
import datetime
import os
import re
import sys


def clear_screen():
    """To clear the screen."""
    try:
      os.system('cls')
    except:
      os.system('clear')


def start_work_log():
    """To start the app."""
    clear_screen()
    greet_user()
    show_menu()


def show_home_menu():
    """This displays the main menu for the app."""
    clear_screen()
    greet_user()
    show_menu()


def greet_user():
    """Greet and welcome the user to the program."""
    current_time = datetime.datetime.now()
    if current_time.hour < 12:
        print(" Good morning, and welcome to the Work Log System.\n")
    elif 12 <= current_time.hour < 18:
        print(" Good afternoon, and welcome to the Work Log System.\n")
    else:
        print(" Good evening, and welcome to the Work Log System.\n")


def show_menu():
    """A menu to choose to add a new entry or lookup previous entries."""
    while True:
        # clear_screen()
        print(" " + "-"*6 + " MENU " + "-"*6)
        print(" [A]dd a new entry")
        print(" [L]ookup previous entries")
        print(" [Q]uit")
        menu_option = input("\n What would you like to do from the menu? ").strip()

        if menu_option.upper() in "ALQ":
            if menu_option.upper() == 'A':
                add_new_work_log()
                break
            elif menu_option.upper() == 'L':
                show_previous_entries_menu()
                break
            elif menu_option.upper() == 'Q':
                input("\n Thank you for using the Work Log System! Press enter to quit. ")
                clear_screen()
                sys.exit
                break
        else:
            input("\n That was an invalid option. Please choose from the menu. Enter either 'A', 'L', or 'Q', and press enter to continue... ")
            start_work_log()
            break


def add_new_work_log():
    """Ask the user for a task name, number of minutes spent working on the task,
    and any additional notes they want on record for this entry."""
    clear_screen()
    print(" " + "-"*6 + " Add New Work Log " + "-"*6)
    print("\n Enter 'H' to go back. ")
    while True:
        task_name = input("\n What would you like to name the task? ").strip()
        # Check to see if task_name is not empty
        if not task_name:
            input(" The task name can't be empty. Press enter to continue... ")
            continue
        elif task_name.upper() == "H":
            show_home_menu()
            break
        else:
            # when task_name has an input other than "H"
            break
    task_duration = ask_for_duration()
    task_date = ask_for_date()

    while True:
        have_remark = input("\n Do you have any comments for this task? [Y]es / [N]o ").strip()
        if have_remark.upper() in "YN":
            if have_remark.upper() == 'Y':
                while True:
                    task_remark = input("\n Add your comment: ").strip()
                    if task_remark:
                        break
                    else:
                        input(" You said you had a comment. Press enter and add it... ")
                        continue
                break
            elif have_remark.upper() == 'N':
                task_remark = "None"
                break
        else:
            input(" That was an invalid input. 'Y' for Yes and 'N' for No. Press enter to answer.")
            continue

    show_entry_summary(task_name, task_duration, task_date, task_remark)


def ask_for_date():
    """Asks for date and validates it"""
    while True:
        task_date = input("\n When was this task performed? Date format: dd-mm-yyyy ").strip()
        try:
            task_date = datetime.datetime.strptime(task_date, "%d-%m-%Y")
            if task_date.date() > datetime.datetime.today().date():
                input(" Sorry, the date can't be later than today's date. Press enter and provide the correct date. ")
                continue
        except ValueError:
            input(" Sorry, not a valid date. Press enter and provide a correct date... ")
            continue
        else:
            return task_date.strftime("%d-%m-%Y")
            break


def ask_for_duration():
    """Asks for valid task duration not more than 24 hours"""
    while True:
        duration = input("\n What's the duration? Format: hh:mm ").strip()
        if not re.match(r'^\d{1,2}:\d{2}$', duration):
            input(" Invalid duration. Your duration must be in the format hh:mm. Press enter to continue... ")
            continue
        elif re.match(r'^\d{1,2}:\d{2}$', duration):
            splitted_duration = duration.split(':')
            # check to see if duration is not 0
            if (int(splitted_duration[0]) < 1) and (int(splitted_duration[1]) < 1):
                input(" Your duration cannot be of 0 hour and 0 minute. Press enter to continue... ")
                continue
                # check to see if hour part of time is not more than 24
            elif int(splitted_duration[0]) > 24:
                input(" Your duration cannot be more than 24 hours. Press enter to continue... ")
                continue
                # check to see if duration is not more than 24
            elif (int(splitted_duration[0]) == 24) and (int(splitted_duration[1]) > 0):
                input(" Your duration cannot be more than 24 hours. Press enter to continue... ")
                continue
                # check to see if duration is not more than 24
            elif (int(splitted_duration[0]) == 23) and (int(splitted_duration[1]) > 60):
                input(" Your duration cannot be more than 24 hours. Press enter to continue... ")
                continue
            else:
                task_duration = (int(splitted_duration[0]) * 60) + (int(splitted_duration[1]))
                return task_duration
                break


def show_entry_summary(task, duration, date, remark):
    """Show user what they've entered before it's saved"""
    clear_screen()
    print(" Please verify if all your enteries are correct.\n")
    print(" Task name: {}".format(task)+"\n")
    print(" Duration: {} minutes".format(duration)+"\n")
    print(" Date: {}".format(date)+"\n")
    print(" Remark: {}".format(remark)+"\n")
    confirm_task_entry(task, duration, date, remark)


def show_previous_entries_menu():
    """Presents to the user list of options to search for previous entries."""
    search_options_menu = True
    while search_options_menu:
        clear_screen()
        print(" " + "-"*6 + " Lookup Previous Entries " + "-"*6)
        print(" Search by [D]ate")
        print(" Search by [T]ime spent")
        print(" Search by [R]egex or Text")
        print(" Go back - [H]ome menu")
        menu_option = input("\n How would you like to search? ").strip()
        if menu_option.upper() in "DTRH":
            if menu_option.upper() == "D":
                date_search_method = input("\n Search by [S]pecific date or [R]ange of dates? ")
                if not date_search_method:
                    input("\n Please enter how you want to search. Press enter to continue... ")
                    continue
                if date_search_method.upper() not in "RS":
                    input("\n Please enter either 'S' or 'R'. Press enter to continue... ")
                    continue
                else:
                    if date_search_method.upper() == "S":
                        search_by_specific_date()
                        break
                    if date_search_method.upper() == "R":
                        search_by_date_range()
                        break
            elif menu_option.upper() == "T":
                search_by_time()
                break
            elif menu_option.upper() == "R":
                search_by_text_regex()
                break
            elif menu_option.upper() == "H":
                show_home_menu()
                break
        else:
            input("\n That was an invalid input. Choose from the menu. Press enter to continue... ")
            continue


def confirm_task_entry(task, duration, date, remark):
    """Ask user whether to save or edit entries"""
    while True:
        summary_response = input("\n [S]ave or [E]dit or [D]elete entries? ")
        if not summary_response:
            input(" Please save with 'S' or edit with 'E'. Press enter to continue... ")
            continue
        if summary_response.upper() not in "SDE":
            input("\n That was an invalid input. Press enter to continue... ")
            continue
        elif summary_response.upper() == 'S':
            save_entry(task, duration, date, remark)
            break
        elif summary_response.upper() == 'D':
            while True:
                delete_confirmation = input("\n Are you sure you want to delete, [Y]es or [N]o? ")
                if not delete_confirmation:
                    input("\n Please confirm whether to delete or not. Press enter to continue... ")
                    continue
                elif delete_confirmation.upper() in "YN":
                    if delete_confirmation.upper() == 'Y':
                        task, duration, date, remark = (None,)*4
                        show_home_menu()
                        break
                    elif delete_confirmation.upper() == 'N':
                        clear_screen()
                        show_entry_summary(task, duration, date, remark)
                        break
                else:
                    input("\n That was an invalid input. Please use either 'Y' or 'N'. Press enter to continue... ")
        elif summary_response.upper() == 'E':
            edit_entry(task, duration, date, remark)
            break


def edit_entry(task, duration, date, remark):
    """Allows the user to edit their entry"""
    clear_screen()
    print(" " + "-"*6 + " Edit Entry " + "-"*6)
    entry_items = (task, duration, date, remark)
    for entry_item in entry_items:
        if entry_item == entry_items[0]:
            while True:
                clear_screen()
                edit_response = input(" Would you like to edit the task name? [Y]es / [N]o? ").strip()
                if edit_response.upper() in "YN":
                    if edit_response.upper() == "Y":
                        clear_screen()
                        print(" " + "-"*3 + " Edit task name " + "-"*3)
                        print("\n Current Task Name: {}".format(task))
                        task = input("\n Edit here: ").strip()
                        break
                    elif edit_response.upper() == "N":
                        break
                else:
                    input("\n That was an invalid input.'Y' for Yes and 'N' for No. Press enter to answer correctly.")
                    continue
        elif entry_item == entry_items[1]:
            while True:
                clear_screen()
                edit_response = input(" Would you like to edit the duration? [Y]es / [N]o? ").strip()
                if edit_response.upper() in "YN":
                    if edit_response.upper() == "Y":
                        clear_screen()
                        print(" " + "-"*3 + " Edit duration " + "-"*3)
                        print("\n Current Duration: {} minutes".format(duration))
                        duration = ask_for_duration()
                        break
                    elif edit_response.upper() == "N":
                        break
                else:
                    input("\n That was an invalid input.'Y' for Yes and 'N' for No. Press enter to answer correctly.")
                    continue
        elif entry_item == entry_items[2]:
            while True:
                clear_screen()
                edit_response = input(" Would you like to edit the date? [Y]es / [N]o? ").strip()
                if edit_response.upper() in "YN":
                    if edit_response.upper() == "Y":
                        clear_screen()
                        print(" " + "-"*3 + " Edit duration " + "-"*3)
                        print("\n Current Duration: {} minutes".format(date))
                        date = ask_for_date()
                        break
                    elif edit_response.upper() == "N":
                        break
                else:
                    input("\n That was an invalid input.'Y' for Yes and 'N' for No. Press enter to answer again.")
                    continue
        elif entry_item == entry_items[3]:
            while True:
                clear_screen()
                edit_response = input(" Would you like to edit the comment? [Y]es / [N]o? ").strip()
                if edit_response.upper() in "YN":
                    if edit_response.upper() == "Y":
                        clear_screen()
                        print(" " + "-"*3 + " Edit comment " + "-"*3)
                        print("\n Current Comment: {}".format(remark))
                        edited_remark = input("\n Edit remark: ").strip()
                        if edited_remark:
                            remark = edited_remark
                            break
                        else:
                            input("You didn't edit your comment. Press enter to continue... ")
                            break
                    elif edit_response.upper() == "N":
                        break
                else:
                    input("\n That was an invalid input.'Y' for Yes and 'N' for No. Press enter to answer again.")
                    continue
    show_entry_summary(task, duration, date, remark)


def save_entry(task, duration, date, remark):
    clear_screen()

    with open('work_log.csv', 'a', newline='') as csvfile:
        entry_fieldnames = ['Task name', 'Duration(minutes)', 'Notes', 'Date']
        filewriter = csv.DictWriter(csvfile, fieldnames=entry_fieldnames)
        filewriter.writerow({
            'Task name': task,
            'Duration(minutes)': duration,
            'Notes': remark,
            'Date': date
        })
    input(" Entry saved! Press enter to continue...")
    show_menu()


def get_all_entries():
    """Reads all the logged entries."""
    with open('work_log.csv', 'r') as csvfile:
        entry_fieldnames = ['Task name', 'Duration(minutes)', 'Notes', 'Date']
        file_reader = csv.DictReader(csvfile, fieldnames=entry_fieldnames)
        entries = list(file_reader)
        return entries


def get_entry_dates(current_entries):
    """Fetches unique dates of entries."""
    searched_dates = []
    for entry in current_entries:
        if entry['Date'] not in searched_dates:
            searched_dates.append(entry['Date'])
    dates = sorted(searched_dates)
    return dates


def print_entry_dates(dates):
    """Prints dates passed to it."""
    print(" " + "-"*3 + " Dates of Entries " + "-"*3)
    for date in dates:
        print("\n" + " "*8 + date)


def search_by_specific_date():
    """Makes a search based on a given date"""
    clear_screen()
    entries = get_all_entries()
    entry_dates = get_entry_dates(entries)
    print_entry_dates(entry_dates)
    searched_entries = []

    while True:
        search_date = input("\n Enter a date (dd-mm-yyyy) to search by: ").strip()
        if not search_date:
            input("\n Please enter a date. Press enter to continue... ")
            continue
        if not re.match(r'[0-9]{2}-[0-9]{2}-[0-9]{4}$', search_date):
            input("\n That was an invalid date. Date must be in the dd-mm-yyyy format. Press enter to continue... ")
            continue
        if search_date not in entry_dates:
            input("\n Please enter valid date. Pick a date from above. Press enter to continue... ")
            continue
        else:
            for entry in entries:
                if entry['Date'] == search_date:
                    searched_entries.append(entry)
            display_searched_results(searched_entries)
            break


def search_by_date_range():
    """Makes a search based on a given date range"""
    clear_screen()
    entries = get_all_entries()
    entry_dates = get_entry_dates(entries)
    searched_entries = []
    search_dates = []

    while True:
        clear_screen()
        print_entry_dates(entry_dates)
        print("\n\n " + " "*3 + "-"*3 + " Go back with -B- " + "-"*3)
        date_range = input("\n Enter a date range (dd-mm-yyyy to dd-mm-yyyy) to search by: ")
        if not date_range:
            input("\n Please enter a date range. Press enter to continue... ")
            continue
        if date_range.upper() == "-B-":
            show_previous_entries_menu()
            break
        if not re.match(r'[0-9]{2}-[0-9]{2}-[0-9]{4}\s?to\s?[0-9]{2}-[0-9]{2}-[0-9]{4}$', date_range):
            input("\n That was an invalid date range. Date must be in the dd-mm-yyyy format. Press enter to continue... ")
            continue
        else:
            # Strip off spaces before and after the "to" after the split.
            date_range = [date.strip() for date in date_range.split("to")]
            if date_range[0] not in entry_dates or date_range[-1] not in entry_dates:
                input("\n Sorry, the date range must be within the above dates. Press enter to continue... ")
                continue
            for entry_date in entry_dates:
                if (entry_date >= date_range[0]) and (entry_date <= date_range[-1]):
                    search_dates.append(entry_date)
            for entry in entries:
                if entry['Date'] in search_dates:
                    searched_entries.append(entry)
            display_searched_results(searched_entries)
            break


def search_by_time():
    """Search by a specific time"""
    clear_screen()
    entries = get_all_entries()
    entry_durations = []
    searched_entries = []
    converted_durations = []
    for entry in entries:
        duration_in_minutes = entry['Duration(minutes)']
        duration_in_minutes = int(duration_in_minutes)
        duration = datetime.timedelta(minutes=duration_in_minutes)
        duration = str(duration)
        duration = duration[:-3]
        if duration not in converted_durations:
            converted_durations.append(duration)

    while True:
        clear_screen()
        print("\n " + "-"*3 + " Current Task Durations " + "-"*3)
        for duration in converted_durations:
            print(" "*13 + duration + " ")

        search_time = ask_for_duration()
        search_time = str(search_time)
        for entry in entries:
            # print("\n Search time: {} VS Entry Duration: {}".format(search_time, entry['Duration(minutes)']))
            if (entry['Duration(minutes)'] == search_time):
                searched_entries.append(entry)
        if not searched_entries:
            input("\n Sorry, there is no task available within that duration. Press enter to continue... ")
            continue
        else:
            display_searched_results(searched_entries)
            break


def search_by_text_regex():
    """Searches the entries by any string or regular expression from the user."""
    entries = get_all_entries()
    while True:
        clear_screen()
        print(" " + "-"*6 + " Search by Text or Regular expression " + "-"*6)
        print("\n\n " + " "*10 + "-"*3 + " Go back with -B- " + "-"*3)
        searched_entries = []
        search_input = input("\n\n Enter your text or regular expression: ")
        if not search_input:
            input("\n You didn't enter anything. Press enter and try again. ")
            continue
        if search_input.upper() == "-B-":
            show_previous_entries_menu()
            break
        else:
            search_token = r'' + search_input
            for entry in entries:
                if (re.search(search_token, entry['Task name']) or
                    re.search(search_token, entry['Notes'])):
                    if entry not in searched_entries:
                        searched_entries.append(entry)
            # print(searched_entries)
            if not searched_entries:
                input("\n Sorry, no results by your search. Press enter and try again... ")
                search_by_text_regex()
            else:
                display_searched_results(searched_entries)
            break


def display_searched_results(searched_entries):
    clear_screen()
    searched_results_page = True
    while searched_results_page:
        index = 0
        while True:
            page_controler = ['[N]ext', '[P]revious', '[B]ack to menu']
            searched_item = searched_entries[index]
            clear_screen()
            # Print a heading for the results.
            print("\n " + "-"*3 + " Search Results " + "-"*3)
            print(" Task name: {}\n"
                  " Duration: {} minutes\n"
                  " Notes: {}\n"
                  " Date: {}\n".format(
                  searched_item['Task name'],
                  searched_item['Duration(minutes)'],
                  searched_item['Notes'],
                  searched_item['Date']))
            # Disable the [P]revious option at the first instance of the results.
            if index == 0:
                page_controler.remove('[P]revious')
            # Disable the [N]ext option at the last instance of the results..
            if index == len(searched_entries) - 1:
                page_controler.remove('[N]ext')
            page_options = ', '.join(page_controler) + ': '
            navigate = input("\n Options: " + page_options).strip()
            if navigate.upper() in "NPB" and navigate.upper() in page_options:
                if navigate.upper() == "P":
                    index -= 1
                    continue
                elif navigate.upper() == "N":
                    index += 1
                    continue
                elif navigate.upper() == "B":
                    break
                else:
                    input("\n Invalid input. Please use the available options. Press enter to continue... ")
                    continue
            if navigate.upper() not in "NPB" and navigate.upper() not in page_options:
                input("\n Invalid input. Please use the available options. Press enter to continue... ")
                continue
        # Break out of the outter loop
        if searched_results_page == True:
            break
    # Show previous menu when navigate.upper() == "B".
    show_previous_entries_menu()


if __name__ == "__main__":
    start_work_log()