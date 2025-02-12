import gspread
from google.oauth2.service_account import Credentials 
from datetime import datetime 

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
] 

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Python Project')
habits = SHEET.worksheet('habits')
completion_data = SHEET.worksheet('percentage of completion')  
start_dates = SHEET.worksheet('start dates')

def get_habit_data():
    """
    Get habit data for the user.
    """
    while True:
        print("Please Enter an option below")
        print("1. Enter a new habit")
        print("2. View all habits")
        print("3. Delete a habit")
        print("4. View completion percentage for a habit")
        print("5. View habit progress (start date and success percentage)")
        print("6. Exit\n")
        data_str = input("Enter your choice here: ")
        
        if data_str == "1":
            enter_new_habit()
        elif data_str == "2":
            view_all_habits()
        elif data_str == "3":
            delete_habit()
        elif data_str == "4":
            view_completion_percentages()
        elif data_str == "5":
            view_habit_progress()
        elif data_str == "6":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

def enter_new_habit():
    new_habit = input("Enter the name of your new habit: ")
    new_habit_lower = new_habit.lower()  # Convert the habit name to lowercase
    habits.append_row([new_habit_lower])  # Store the habit in lowercase
    print(f"Habit '{new_habit}' added successfully!")

def view_all_habits():
    all_habits = habits.get_all_values()
    if all_habits:
        print("Your habits:")
        for habit in all_habits:
            print(habit[0])
    else:
        print("You have no habits recorded.")

def delete_habit():
    habit_name = input("Enter the name of the habit to delete: ")
    all_habits = habits.get_all_values()
    habit_found = False
    
    for i, habit in enumerate(all_habits):
        if habit[0].lower() == habit_name.lower():  # Case-insensitive comparison
            habits.delete_rows(i + 1)  # Rows are 1-indexed in gspread
            print(f"Habit '{habit[0]}' deleted successfully!")
            habit_found = True
            break
    
    if not habit_found:
        print(f"Habit '{habit_name}' not found.")

def view_completion_percentages():
    habit_name = input("Enter the name of the habit you want the completion percentage for: ")
    completion_records = completion_data.get_all_values()
    
    habit_found = False
    for record in completion_records:
        if record[0].lower() == habit_name.lower():  # Case-insensitive comparison
            completion_percentage = record[1]
            print(f"Completion percentage for '{record[0]}': {completion_percentage}%")
            habit_found = True
            break
    
    if not habit_found:
        print(f"No completion data found for habit '{habit_name}'.")


def view_habit_progress():
    habit_name = input("Enter the name of the habit you want to check progress for: ")
    habit_name_lower = habit_name.lower()  
    start_dates_records = start_dates.get_all_values()
    habit_found = False

    for record in start_dates_records:
        if record[0].lower() == habit_name_lower:  
            start_date_str = record[1] 
            habit_found = True
            break

    if not habit_found:
        print(f"No start date found for habit '{habit_name}'.")
        return


    completion_records = completion_data.get_all_values()
    success_percentage = None

    for record in completion_records:
        if record[0].lower() == habit_name_lower:  
            success_percentage = record[1]  
            break

    if not success_percentage:
        print(f"No completion data found for habit '{habit_name}'.")
        return


    try:
        start_date = datetime.strptime(start_date_str, "%d/%m/%Y") 
        current_date = datetime.now()  
        days_since_start = (current_date - start_date).days 
    except ValueError:
        print(f"Invalid date format for habit '{habit_name}'. Expected format: DD/MM/YYYY.")
        return

    print(f"\nHabit: {habit_name}")
    print(f"Start Date: {start_date.strftime('%d/%m/%Y')}")
    print(f"Days since start: {days_since_start} days")
    print(f"Success Percentage: {success_percentage}%\n")


get_habit_data()