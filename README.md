# Smart Expense Tracker

A simple desktop application to record and manage daily expenses.
Built with Python, Tkinter, SQLite and CSV.

## Features
- Add an expense (date, category, description, amount)
- View all expenses in a table
- Total spending calculated automatically
- Delete a selected expense (with confirmation)
- Export expenses to a CSV file (share via WhatsApp or email)
- Data saved permanently in a local SQLite database

## Requirements
- Python 3.8 or newer
- No extra libraries needed (Tkinter, sqlite3 and csv come with Python)

## How to Run
1. Put `main.py` and `README.md` in a folder named `SmartExpenseTracker`.
2. Open a terminal / command prompt in that folder.
3. Run:

       python main.py

The file `expenses.db` is created automatically on first run.

## How to Use
1. Enter the date (YYYY-MM-DD), category, description and amount.
2. Click **Add Expense**.
3. Select a row and click **Delete Selected** to remove it.
4. Click **Export CSV** to save all records as a CSV file.

## Sharing
Each person has their own local `expenses.db`. To share records, export a
CSV file and send it through WhatsApp or email.

## Technologies
Python, Tkinter, SQLite3, CSV