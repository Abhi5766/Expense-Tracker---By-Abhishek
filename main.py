#Expense Tracker By Abhishek

import csv
import os
import sqlite3
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox, ttk

# The database file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "expenses.db")

CATEGORIES = ["Food", "Travel", "Shopping", "Bills", "Education",
            "Health", "Entertainment", "Other"]

# Simple colour scheme
BG_COLOR = "#f4f6f8"
HEADER_COLOR = "#2c3e50"
BUTTON_ADD = "#27ae60"
BUTTON_DELETE = "#c0392b"
BUTTON_EXPORT = "#2980b9"


# Database functions

def init_db():
    """Create the database and table if they do not exist."""
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS expenses (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                date        TEXT NOT NULL,
                category    TEXT NOT NULL,
                description TEXT,
                amount      REAL NOT NULL
            )
            """
        )


def db_add_expense(date, category, description, amount):
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(
            "INSERT INTO expenses (date, category, description, amount) "
            "VALUES (?, ?, ?, ?)",
            (date, category, description, amount),
        )


def db_get_expenses():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.execute(
            "SELECT id, date, category, description, amount "
            "FROM expenses ORDER BY date DESC, id DESC"
        )
        return cursor.fetchall()


def db_delete_expense(expense_id):
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))


def db_get_total():
    with sqlite3.connect(DB_FILE) as conn:
        result = conn.execute("SELECT SUM(amount) FROM expenses").fetchone()[0]
        return result if result is not None else 0.0


# Main application code
class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Expense Tracker")
        self.root.geometry("820x600")
        self.root.minsize(760, 520)
        self.root.configure(bg=BG_COLOR)

        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.category_var = tk.StringVar()
        self.description_var = tk.StringVar()
        self.amount_var = tk.StringVar()
        self.total_var = tk.StringVar(value="Total Expenses: Rs. 0.00")

        self.build_title()
        self.build_input_form()
        self.build_buttons()
        self.build_table()
        self.build_total()

        self.refresh_table()

#GUI Code 
    def build_title(self):
        title = tk.Label(
            self.root, text="Smart Expense Tracker",
            font=("Segoe UI", 20, "bold"),
            bg=HEADER_COLOR, fg="white", pady=12,
        )
        title.pack(fill="x")

    def build_input_form(self):
        form = tk.LabelFrame(
            self.root, text=" Add New Expense ",
            font=("Segoe UI", 10, "bold"), bg=BG_COLOR, padx=15, pady=10,
        )
        form.pack(fill="x", padx=15, pady=(15, 5))

        label_font = ("Segoe UI", 10)

        tk.Label(form, text="Date (YYYY-MM-DD):", font=label_font,
                bg=BG_COLOR).grid(row=0, column=0, sticky="w", pady=5)
        tk.Entry(form, textvariable=self.date_var, font=label_font,
                width=22).grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form, text="Category:", font=label_font,
                bg=BG_COLOR).grid(row=0, column=2, sticky="w", pady=5)
        ttk.Combobox(form, textvariable=self.category_var, values=CATEGORIES,
                    font=label_font, width=20).grid(row=0, column=3,
                                                padx=10, pady=5)

        tk.Label(form, text="Description:", font=label_font,
                bg=BG_COLOR).grid(row=1, column=0, sticky="w", pady=5)
        tk.Entry(form, textvariable=self.description_var, font=label_font,
                width=22).grid(row=1, column=1, padx=10, pady=5)

        tk.Label(form, text="Amount (Rs.):", font=label_font,
                bg=BG_COLOR).grid(row=1, column=2, sticky="w", pady=5)
        tk.Entry(form, textvariable=self.amount_var, font=label_font,
                width=22).grid(row=1, column=3, padx=10, pady=5)

    def build_buttons(self):
        frame = tk.Frame(self.root, bg=BG_COLOR)
        frame.pack(fill="x", padx=15, pady=10)

        button_font = ("Segoe UI", 10, "bold")

        tk.Button(frame, text="Add Expense", command=self.add_expense,
                font=button_font, bg=BUTTON_ADD, fg="white",
                width=16, relief="flat", cursor="hand2").pack(side="left", padx=5)

        tk.Button(frame, text="Delete Selected", command=self.delete_expense,
                font=button_font, bg=BUTTON_DELETE, fg="white",
                width=16, relief="flat", cursor="hand2").pack(side="left", padx=5)

        tk.Button(frame, text="Export CSV", command=self.export_csv,
                font=button_font, bg=BUTTON_EXPORT, fg="white",
                width=16, relief="flat", cursor="hand2").pack(side="left", padx=5)

    def build_table(self):
        frame = tk.Frame(self.root, bg=BG_COLOR)
        frame.pack(fill="both", expand=True, padx=15, pady=5)

        style = ttk.Style()
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=26)
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

        columns = ("id", "date", "category", "description", "amount")
        self.table = ttk.Treeview(frame, columns=columns,
                                show="headings", selectmode="browse")

        self.table.heading("id", text="ID")
        self.table.heading("date", text="Date")
        self.table.heading("category", text="Category")
        self.table.heading("description", text="Description")
        self.table.heading("amount", text="Amount (Rs.)")

        self.table.column("id", width=50, anchor="center")
        self.table.column("date", width=110, anchor="center")
        self.table.column("category", width=130, anchor="center")
        self.table.column("description", width=320, anchor="w")
        self.table.column("amount", width=110, anchor="e")

        scrollbar = ttk.Scrollbar(frame, orient="vertical",
                                command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)

        self.table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def build_total(self):
        tk.Label(self.root, textvariable=self.total_var,
                font=("Segoe UI", 14, "bold"),
                bg=BG_COLOR, fg=HEADER_COLOR, pady=10).pack()

    # ---------------- Actions ----------------
    def refresh_table(self):
        """Reload all rows from the database and update the total."""
        for row in self.table.get_children():
            self.table.delete(row)

        for expense in db_get_expenses():
            expense_id, date, category, description, amount = expense
            self.table.insert("", "end",
                            values=(expense_id, date, category,
                                    description, f"{amount:.2f}"))

        self.total_var.set(f"Total Expenses: Rs. {db_get_total():.2f}")

    def add_expense(self):
        date = self.date_var.get().strip()
        category = self.category_var.get().strip()
        description = self.description_var.get().strip()
        amount_text = self.amount_var.get().strip()

        # Validate date
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Invalid Date",
                                "Please enter the date as YYYY-MM-DD "
                                "(example: 2026-10-15).")
            return

        # Validate category
        if not category:
            messagebox.showerror("Missing Category",
                                "Please enter or select a category.")
            return

        # Validate amount
        try:
            amount = float(amount_text)
        except ValueError:
            messagebox.showerror("Invalid Amount",
                                "Amount must be a number (example: 250.50).")
            return
        if amount <= 0:
            messagebox.showerror("Invalid Amount",
                                "Amount must be greater than zero.")
            return

        try:
            db_add_expense(date, category, description, amount)
        except sqlite3.Error as error:
            messagebox.showerror("Database Error",
                                f"Could not save the expense.\n{error}")
            return

        # Clear fields ka yaha se hai
        self.category_var.set("")
        self.description_var.set("")
        self.amount_var.set("")
        self.refresh_table()
        messagebox.showinfo("Success", "Expense added successfully.")

    def delete_expense(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showwarning("No Selection",
                                "Please select an expense to delete.")
            return

        expense_id = self.table.item(selected[0])["values"][0]

        if messagebox.askyesno("Confirm Delete",
                            "Are you sure you want to delete "
                            "the selected expense?"):
            try:
                db_delete_expense(expense_id)
            except sqlite3.Error as error:
                messagebox.showerror("Database Error",
                                    f"Could not delete the expense.\n{error}")
                return
            self.refresh_table()

    def export_csv(self):
        expenses = db_get_expenses()
        if not expenses:
            messagebox.showwarning("No Data", "There are no expenses to export.")
            return

        default_name = f"expenses_{datetime.now().strftime('%Y%m%d')}.csv"
        file_path = filedialog.asksaveasfilename(
            title="Export Expenses",
            defaultextension=".csv",
            initialfile=default_name,
            filetypes=[("CSV files", "*.csv")],
        )
        if not file_path:  # user cancelled 
            return

        try:
            with open(file_path, "w", newline="", encoding="utf-8-sig") as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Date", "Category",
                                "Description", "Amount"])
                writer.writerows(expenses)
                writer.writerow([])
                writer.writerow(["", "", "", "Total", f"{db_get_total():.2f}"])
        except OSError as error:
            messagebox.showerror("Export Error",
                                f"Could not save the file.\n{error}")
            return

        messagebox.showinfo("Export Successful",
                            f"Expenses exported to:\n{file_path}\n\n"
                            "You can now share this file through "
                            "WhatsApp or email.")



# Program entry 

def main():
    init_db()
    root = tk.Tk()
    ExpenseTrackerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()