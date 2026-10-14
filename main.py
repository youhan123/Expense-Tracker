import os
import sqlite3
from datetime import datetime

#Connect to the database (this automatically creates 'expenses.db' if it doesn't exist)
conn = sqlite3.connect("expenses.db")
#This makes the database return rows that act like dictionaries!
conn.row_factory = sqlite3.Row 
cursor = conn.cursor()

def setup_database():
    #Write an SQL query to create our table with specific data types
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            description TEXT,
            amount REAL
        )
    ''')
    conn.commit() # Always commit changes to save them

def clear_screen():
    # 'nt' is Windows. If it's Windows, use 'cls', otherwise use 'clear'
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input("\nPress Enter to continue...")
    clear_screen()

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

    cursor.execute('''
            INSERT INTO expenses (date, category, description, amount)
            VALUES (?, ?, ?, ?)
        ''', (date, category, desc, amount))
        
    conn.commit()

    print("Expenses added successfully!")

def view_expenses():
    print("\n"+"="*80)
    print("Expenses".center(80))
    print("="*80)

    # SQL SELECT: Grab everything
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()

    if not rows:
        print("No expenses recorded.")
        return False # Return False so edit/delete know it's empty

    print(f"{'ID':<5} | {'Date':<12} | {'Description':<20} | {'Amount':<12} | {'Category':<20}")
    print("-" * 80)

    for row in rows:
        print(f"{row['id']:<5} | {row['date']:<12} | {row['description']:<20} | RM {row['amount']:<9.2f} | {row['category']:<20}")
    
    return True

def edit_expense():
    if not view_expenses():
        return
    
    while True:
        choice = input("\nPlease select the ID of the expense you want to edit ( or q to cancel ): ")

        if choice.lower() == 'q':
            print("Cancelled edit process")
            break

        try:
            item_no = int(choice)
            cursor.execute("SELECT * FROM expenses WHERE id = ?", (item_no,))
            target = cursor.fetchone()

            if not target:
                print("ID not found. Please enter a valid ID from the table.")
                continue
            
            edit_category = input("Please type the category you want to edit (eg. Date/Description/Amount): ")

            if edit_category.lower() == 'date':
                while True:
                    new_date = input("Enter new date: ")
                    try:
                        datetime.strptime(new_date,"%d/%m/%Y")
                        cursor.execute("UPDATE expenses SET date = ? WHERE id = ?", (new_date, item_no))
                        conn.commit()
                        print("Edit Success!")
                        break
                    except ValueError:
                        print("Invalid date format. Please exactly match DD/MM/YYYY.")

            elif edit_category.lower() == 'description' :
                new_description = input("Enter new description: ")
                cursor.execute("UPDATE expenses SET description = ? WHERE id = ?", (new_description, item_no))
                conn.commit()
                print("Edit Success!")
                break

            elif edit_category.lower() == 'amount' :
                new_amount = input("Enter new amount (RM) : ")
                try:
                    new = float(new_amount)

                    if new <0 :
                        print("Edit failed, Please enter positive number")

                    else:
                        cursor.execute("UPDATE expenses SET amount = ? WHERE id = ?", (new, item_no))
                        conn.commit()
                        print("Edit success!")
                        break

                except ValueError:
                    print("Edit failed, please enter valid input")


        except ValueError:
            print("Please enter a valid input")

def delete_expense():
    if not view_expenses():
        return
    view_expenses()

    while True:
        choice = input("Please select the expense number to delete ( or q to cancel ): ")
        if choice.lower() == 'q':
            print("deletion cancelled")
            break

        try: 
            item_no = int(choice)
            # Check if the ID exists and fetch it so we can print the success message
            cursor.execute("SELECT description, amount FROM expenses WHERE id = ?", (item_no,))
            target = cursor.fetchone()

            if not target:
                print("ID not found. Please enter a valid ID from the table.")
                continue
                
            cursor.execute("DELETE FROM expenses WHERE id = ?", (item_no,))
            conn.commit()
            print(f"Success! Deleted {target['description']} (RM {target['amount']})")
            break

        except ValueError:
            print("Please enter a valid numeric ID.")

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

    if choice == '1':
        # View All: Just use the master list
        cursor.execute("SELECT * FROM expenses")

    elif choice == '2':
        # Filter by Month
        month = input("Enter month (MM) e.g., 10 : ")
        # Using SQL wildcards. _ means any character. __/MM/____ perfectly matches DD/MM/YYYY
        cursor.execute("SELECT * FROM expenses WHERE date LIKE ?", (f"__/{month}/____",))

    elif choice == '3':
        # Filter by Category
        print("1. Food and Beverages | 2. Billings | 3. Entertainment | 4. Others")
        cat_choice = input("Enter category number (1-4): ")
        
        # Map the number to the exact string used in your add_expense function
        cat_menu = {'1': 'Food and Beverages', '2': 'Billings', '3': 'Entertainment', '4': 'Others'}
        selected_cat = cat_menu.get(cat_choice)
        
        if selected_cat:
            cursor.execute("SELECT * FROM expenses WHERE category = ?", (selected_cat,))
        else:
            print("Invalid category selection.")
            return
            
    else:
        print("Invalid choice.")
        return

    # Fetch the results based on whichever query ran above
    rows = cursor.fetchall()

    if not rows:
        print("\nNo expenses found for this filter.")
        return

    # Print the filtered items neatly
    print("\n"+"=" * 75)
    print(f"{'Date':<12} | {'Category':<20} | {'Description':<20} | {'Amount'}")
    print("=" * 75)
    for row in rows:
        print(f"{row['date']:<12} | {row['category']:<20} | {row['description']:<20} | RM {row['amount']:<10.2f}")

    calculate_total(rows)

def main():
    setup_database()
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
            conn.close()
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()