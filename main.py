import json

expenses_file = "expenses.json"
expenses = [] 

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
    print("======================")
    print("     Add Expenses     ")
    print("======================")
    date = input("Enter date (DD/MM/YYYY) : ")
    desc = input("Enter description")

    while True:
        amount_text = input("Enter expense amount (RM x) : ")
        try:
            amount = float(amount_text)
            break
        except ValueError:
            print("Please enter a valid input")

    new_expense = {"date" : date,
                   "amount" : amount,
                   "desc" : desc}

    expenses.append(new_expense)
    save_expenses()

    print("Expenses added successfully!")

def view_expenses():
    print("======================")
    print("    View Expenses     ")
    print("======================")

    if not expenses:
        print("No expenses recorded.")
        return

    print(f"{'No.':<5} | {'Date':<12} | {'Description':<20} | {'Amount'}")
    print("-" * 70)

    for i, expense in enumerate(expenses, start=1):
        date = expense['date']
        desc = expense['desc']
        amount = expense['amount']
        
        print(f"{i:<5} | {date:<12} | {desc:<20} | RM {amount:<10.2f}")

def edit_expense():
    view_expenses()

    while True:
        choice = input("Please select the expense you want to edit ( or q to cancel ): ")

        if choice.lower() == 'q':
            print("Cancelled edit process")
            break

        try:
            item_no = int(choice)

            if item_no <= 0 or item_no > len(expenses) :
                print("please enter a valid range")

            else:
                edit_category = input("Please type the category you want to edit (eg. Date/Description/Amount): ")

                if edit_category.lower() == 'date':
                    new_date = input("Enter new date: ")
                    expenses[item_no-1]['date'] = new_date
                    print("Edit Success!")
                    save_expenses()
                    break

                elif edit_category.lower() == 'description' :
                    new_description = input("Enter new description: ")
                    expenses[item_no-1]['desc'] = new_description
                    print("Edit success!")
                    save_expenses()
                    break

                elif edit_category.lower() == 'amount' :
                    new_amount = input("Enter new amount (RM)")
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
    print("======================")
    print("    Delete Expenses   ")
    print("======================")

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

def calculate_total():
    total = 0

    for expense in expenses:
        total+= expense['amount']
        
    print(f"\nTotal Expenses: RM {total:.2f}")

def main():
    load_expenses()
    while True:
        print("\n--- Expense Tracker ---")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Edit Expense")
        print("4. Delete Expense")
        print("5. View Total")
        print("6. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            edit_expense()
        elif choice == '4':
            delete_expense()
        elif choice == '5':
            calculate_total()
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()