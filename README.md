# Expense-Tracker
Python CLI Expense Tracker

A lightweight, command-line personal expense tracker built entirely in Python. This application allows users to easily log, edit, view, and delete their daily expenses, keeping track of their financial spending directly from the terminal.
It features data persistence, meaning all your expenses are safely saved to a local file and will still be there the next time you open the app!

Features
Add Expenses: Log new expenses with a date, description, and amount (RM).
View Expenses: See a neatly formatted table of all your recorded expenses.
Edit Expenses: Update the date, description, or amount of any existing record.
Delete Expenses: Remove an expense from your list using its ID.
Calculate Total: Instantly sum up all your recorded expenses to see your total spending.
Data Persistence: Automatically saves and loads your data using a local expenses.json file.
Error Handling: Prevents crashes from invalid inputs (e.g., typing text when a number is required).

Prerequisites:
Python 3.x installed on your machine.
No external libraries are required! This project uses only Python's built-in json module.

How to Run:
Open your terminal (or command prompt/PowerShell).
Navigate to the folder where you saved the project.
Run the following command:
python main.py
(Note for Windows users: If the above command doesn't work, try py main.py)

Usage Guide:
Once the program starts, you will be greeted with a main menu:
Type 1 to add a new expense. The system will prompt you for the Date, Description, and Amount.
Type 2 to view your current list of expenses. Take note of the "No." column, as you will need this ID to edit or delete items.
Type 3 to edit an expense. You will be asked for the expense ID and which field you want to update.
Type 4 to delete an expense using its ID.
Type 5 to view the total sum of all your expenses.
Type 6 to safely exit the application.

Structure:
main.py: The main application code containing all the logic and loops.
expenses.json: The database file where your expenses are saved (this file is generated automatically when you add your first expense).