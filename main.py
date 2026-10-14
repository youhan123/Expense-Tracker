import json
import os
from datetime import datetime

expenses_file = "expenses.json"
expenses = [] 

def clear_screen():
    # 'nt' is Windows. If it's Windows, use 'cls', otherwise use 'clear'
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input("\nPress Enter to continue...")
    clear_screen()

def load_expenses():
    global expenses
    try:
        # 'r' means read mode
        with open(expenses_file, "r") as file:
            expenses = json.load(file)
    except FileNotFoundError:
        # If it's the first time running the app, the file won't exist yet
        expenses = []
    except json.JSONDecodeError:
        # If the file is empty or corrupted
        expenses = []

def save_expenses():
    # 'w' means write mode (overwrites the file with new data)
    with open(expenses_file, "w") as file:
        json.dump(expenses, file, indent=4)

def add_expense():
    print("\n" + "="*30)
    print("Add Expenses".center(30))
    print("="*30)

    while True:
        date = input("Enter date (DD/MM/YYYY) : ")
        try:
            datetime.strptime(date, "%d/%m/%Y")
            break
        except ValueError:
            print("Invalid date format. Please exactly match DD/MM/YYYY.")

# Map the numbers directly to the names
    cat_menu = {
        1: "Food and Beverages", 
        2: "Billings", 
        3: "Entertainment", 
        4: "Others"
    }

    while True:
        print("\n" +"="*30)
        print("Expense Category".center(30))
        print("="*30)
        print("1. Food and Beverages")
        print("2. Billings ")
        print("3. Entertainment ")
        print("4. Others")

        option = input("\nPlease select expense category(1,2,3,4): ")

        try:
            cat = int(option)
            if cat in cat_menu:
                category = cat_menu[cat] 
                break
            else:
                print("Try again, please select 1, 2, 3, or 4")
                
        except ValueError:
            print("Try again, please enter valid input! ")
            
    desc = input("Enter description : ")

    while True:
        amount_text = input("Enter expense amount (RM x) : ")
        try:
            amount = float(amount_text)
            break
        except ValueError:
            print("Please enter a valid input")

    new_expense = {"date" : date,
                   "amount" : amount,
                   "category" : category,
                   "desc" : desc}

    expenses.append(new_expense)
    save_expenses()

    print("Expenses added successfully!")

def view_expenses():
    print("\n"+"="*80)
    print("Expenses".center(80))
    print("="*80)

    if not expenses:
        print("No expenses recorded.")
        return

    print(f"{'No.':<5} | {'Date':<12} | {'Description':<20} | {'Amount':<13} | {'category':<20}")
    print("-" * 80)

    for i, expense in enumerate(expenses, start=1):
        date = expense['date']
        desc = expense['desc']
        amount = expense['amount']
        category = expense['category']
        
        print(f"{i:<5} | {date:<12} | {desc:<20} | RM {amount:<10.2f} | {category:<20}")

def edit_expense():
    view_expenses()

    while True:
        choice = input("\nPlease select the no. of the expense you want to edit ( or q to cancel ): ")

        if choice.lower() == 'q':
            print("Cancelled edit process\n")
            break

        try:
            item_no = int(choice)

            if item_no <= 0 or item_no > len(expenses) :
                print("please enter a valid range")

            else:
                edit_category = input("Please type the category you want to edit (eg. Date/Description/Amount): ")

                if edit_category.lower() == 'date':
                    while True:
                        new_date = input("Enter new date: ")
                        try:
                            datetime.strptime(new_date,"%d/%m/%Y")
                            expenses[item_no-1]['date'] = new_date
                            print("Edit Success!")
                            save_expenses()
                            break
                        except ValueError:
                            print("Invalid date format. Please exactly match DD/MM/YYYY.")

                elif edit_category.lower() == 'description' :
                    new_description = input("Enter new description: ")
                    expenses[item_no-1]['desc'] = new_description
                    print("Edit success!")
                    save_expenses()
                    break

                elif edit_category.lower() == 'amount' :
                    new_amount = input("Enter new amount (RM) : ")
                    try:
                        new = float(new_amount)

                        if new <0 :
                            print("Edit failed, Please enter positive number")

                        else:
                            expenses[item_no -1]['amount'] = new
                            print("Edit success!")
                            save_expenses()
                            break

                    except ValueError:
                        print("Edit failed, please enter valid input")


        except ValueError:
            print("Please enter a valid input")

def delete_expense():
    view_expenses()

    while True:
        choice = input("Please select the expense number to delete ( or q to cancel ): ")
        if choice.lower() == 'q':
            print("deletion cancelled")
            break

        try: 
            item_no = int(choice)

            if item_no <0 or item_no > len(expenses):
                print("Please enter number greater than 0")

            else:
                deleted_item = expenses.pop(item_no -1)
                print(f"Success! Deleted {deleted_item['desc']}(RM{deleted_item['amount']})")
                save_expenses()
                break

        except ValueError:
            print("Please enter a valid input")

def calculate_total(data_list):
    total = 0
    for expense in data_list:
        total += expense['amount']
        
    print(f"\nTotal for selected expenses: RM {total:.2f}")

def expenses_summary():
    print("\n======================")
    print("   Expenses Summary   ")
    print("======================")
    print("1. View All")
    print("2. Filter by Month")
    print("3. Filter by Category")
    
    choice = input("Choose a filter option: ")
    filtered_list = []

    if choice == '1':
        # View All: Just use the master list
        filtered_list = expenses

    elif choice == '2':
        # Filter by Month
        month = input("Enter month (MM) e.g., 10 : ")
        for expense in expenses:
            # date format is strictly DD/MM/YYYY
            # .split('/') turns "14/10/2026" into a list: ['14', '10', '2026']
            date_parts = expense['date'].split('/')
            
            # Check if the month (index 1) matches the user's input
            if len(date_parts) == 3 and date_parts[1] == month:
                filtered_list.append(expense)

    elif choice == '3':
        # Filter by Category
        print("1. Food and Beverages | 2. Billings | 3. Entertainment | 4. Others")
        cat_choice = input("Enter category number (1-4): ")
        
        # Map the number to the exact string used in your add_expense function
        cat_menu = {'1': 'Food and Beverages', '2': 'Billings', '3': 'Entertainment', '4': 'Others'}
        selected_cat = cat_menu.get(cat_choice)
        
        if selected_cat:
            for expense in expenses:
                if expense.get('category') == selected_cat:
                    filtered_list.append(expense)
        else:
            print("Invalid category selection.")
            return
            
    else:
        print("Invalid choice.")
        return

    # --- Display the Results ---
    if not filtered_list:
        print("\nNo expenses found for this filter.")
        return

    # Print the filtered items neatly
    print("\n"+"=" * 75)
    print(f"{'Date':<12} | {'Category':<20} | {'Description':<20} | {'Amount'}")
    print("=" * 75)
    for exp in filtered_list:
        # Use .get() for category just in case older saved data doesn't have it
        cat = exp.get('category', 'Uncategorized')
        print(f"{exp['date']:<12} | {cat:<20} | {exp['desc']:<20} | RM {exp['amount']:<10.2f}")

    # Pass our newly created list to the math function!
    calculate_total(filtered_list)

def main():
    load_expenses()
    while True:
        clear_screen()
        print("="*30)
        print("Expense Tracker".center(30))
        print("="*30)
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Edit Expense")
        print("4. Delete Expense")
        print("5. Expenses Summary")
        print("6. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == '1':
            add_expense()
            pause()
        elif choice == '2':
            view_expenses()
            pause()
        elif choice == '3':
            edit_expense()
            pause()
        elif choice == '4':
            delete_expense()
            pause()
        elif choice == '5':
            expenses_summary()
            pause()
        elif choice == '6':
            print("Thanks for using!")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()