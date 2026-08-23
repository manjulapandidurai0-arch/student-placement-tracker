import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Database connection
connection = sqlite3.connect("placement.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT NOT NULL,
    role TEXT NOT NULL,
    status TEXT NOT NULL
)
""")

connection.commit()


def add_application():
    company = company_entry.get()
    role = role_entry.get()
    status = status_box.get()

    if not company or not role:
        messagebox.showwarning("Warning", "Please enter company and role.")
        return

    cursor.execute(
        "INSERT INTO applications (company, role, status) VALUES (?, ?, ?)",
        (company, role, status)
    )

    connection.commit()

    company_entry.delete(0, tk.END)
    role_entry.delete(0, tk.END)

    load_applications()


def load_applications():
    for item in table.get_children():
        table.delete(item)

    cursor.execute("SELECT company, role, status FROM applications")

    for row in cursor.fetchall():
        table.insert("", tk.END, values=row)


# Main window
root = tk.Tk()
root.title("Student Placement Tracker")
root.geometry("750x500")

title = ttk.Label(
    root,
    text="Student Placement Tracker",
    font=("Arial", 20, "bold")
)
title.pack(pady=20)

# Company
ttk.Label(root, text="Company").pack()
company_entry = ttk.Entry(root, width=40)
company_entry.pack(pady=5)

# Role
ttk.Label(root, text="Job Role").pack()
role_entry = ttk.Entry(root, width=40)
role_entry.pack(pady=5)

# Status
ttk.Label(root, text="Application Status").pack()

status_box = ttk.Combobox(
    root,
    values=["Applied", "Shortlisted", "Interview", "Selected", "Rejected"],
    state="readonly"
)
status_box.pack(pady=5)
status_box.current(0)

# Add button
ttk.Button(
    root,
    text="Add Application",
    command=add_application
).pack(pady=15)

# Table
table = ttk.Treeview(
    root,
    columns=("Company", "Role", "Status"),
    show="headings"
)

table.heading("Company", text="Company")
table.heading("Role", text="Job Role")
table.heading("Status", text="Status")

table.pack(fill="both", expand=True, padx=20, pady=20)

load_applications()

root.mainloop()

connection.close()
