import tkinter as tk
from tkinter import ttk
import sqlite3
import random
import string

# Create a database connection
conn = sqlite3.connect('passwords.db')
cursor = conn.cursor()

# Create separate tables for "Search Password" and "Retrieve All Passwords"
cursor.execute('''CREATE TABLE IF NOT EXISTS search_passwords (
                  website TEXT,
                  username TEXT,
                  password TEXT
               )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS retrieve_passwords (
                  website TEXT,
                  username TEXT,
                  password TEXT
               )''')

conn.commit()

def generate_password():
    length = 12
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)

def save_password():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    if not all((website, username, password)):
        warning_lable.config(text="All fields are required.")
        return

    cursor.execute("INSERT INTO search_passwords VALUES (?, ?, ?)", (website, username, password))
    cursor.execute("INSERT INTO retrieve_passwords VALUES (?, ?, ?)", (website, username, password))
    conn.commit()

    website_entry.delete(0, tk.END)
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

    # Display a success message
    success_label.config(text="Saved password successfully!")

def search_password():
    website = website_search_entry.get()
    username = username_search_entry.get()

    if not all((website, username)):
        warning_lable1.config(text="All fields are required.")
        return

    cursor.execute("SELECT * FROM search_passwords WHERE website=? AND username=?", (website, username))
    rows = cursor.fetchall()

    for row in tree_search.get_children():
        tree_search.delete(row)

    for row in rows:
        tree_search.insert("", "end", values=row)

def retrieve_all_passwords(master_key):
    if master_key == 'Ayman098':
        cursor.execute("SELECT * FROM retrieve_passwords")
        rows = cursor.fetchall()

        for row in tree_retrieve.get_children():
            tree_retrieve.delete(row)

        for row in rows:
            tree_retrieve.insert("", "end", values=row)

def verify_master_key():
    entered_key = master_key_entry.get()
    if entered_key == 'Ayman098':
        retrieve_all_passwords(entered_key)
    else:
        master_key_entry.delete(0, tk.END)
        warning_lable2.config(text="Incorrect Key!!!")
        

app = tk.Tk()
app.title("Password Manager")

# Create tabs
tab_control = ttk.Notebook(app)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab3 = ttk.Frame(tab_control)
tab_control.add(tab1, text='Save Password')
tab_control.add(tab2, text='Search Password')
tab_control.add(tab3, text='Retrieve All Passwords')
tab_control.pack(expand=1, fill="both")

# Save Password Tab
website_label = tk.Label(tab1, text="Website")
website_label.grid(row=0, column=0)
website_entry = tk.Entry(tab1)
website_entry.grid(row=0, column=1)

username_label = tk.Label(tab1, text="Username")
username_label.grid(row=1, column=0)
username_entry = tk.Entry(tab1)
username_entry.grid(row=1, column=1)

password_label = tk.Label(tab1, text="Password")
password_label.grid(row=2, column=0)
password_entry = tk.Entry(tab1)
password_entry.grid(row=2, column=1)

generate_button = tk.Button(tab1, text="Generate Password", command=generate_password)
generate_button.grid(row=2, column=2)

save_button = tk.Button(tab1, text="Save Password", command=save_password)
save_button.grid(row=3, column=1)

# Add a label for success message
success_label = tk.Label(tab1, text="", fg="green")
success_label.grid(row=4, column=1)

warning_lable = tk.Label(tab1, text="", fg="red")
warning_lable.grid(row=4, column=1)

warning_lable1 = tk.Label(tab2, text="", fg="red")
warning_lable1.grid(row=4, column=1)

warning_lable2 = tk.Label(tab3, text="", fg="red")
warning_lable2.grid(row=4, column=1)

# Search Password Tab
website_search_label = tk.Label(tab2, text="Website")
website_search_label.grid(row=0, column=0)
website_search_entry = tk.Entry(tab2)
website_search_entry.grid(row=0, column=1)

username_search_label = tk.Label(tab2, text="Username")
username_search_label.grid(row=1, column=0)
username_search_entry = tk.Entry(tab2)
username_search_entry.grid(row=1, column=1)

search_button = tk.Button(tab2, text="Search Password", command=search_password)
search_button.grid(row=2, column=1)

tree_search = ttk.Treeview(tab2, columns=("Website", "Username", "Password"))
tree_search.heading("#1", text="Website")
tree_search.heading("#2", text="Username")
tree_search.heading("#3", text="Password")
tree_search.grid(row=3, column=0, columnspan=3)
tree_search.column("#1", width=200)
tree_search.column("#2", width=150)
tree_search.column("#3", width=200)

# Retrieve All Passwords Tab
master_key_label = tk.Label(tab3, text="Enter Master Key")
master_key_label.grid(row=0, column=0)
master_key_entry = tk.Entry(tab3, show='*')
master_key_entry.grid(row=0, column=1)

retrieve_button = tk.Button(tab3, text="Retrieve All Passwords", command=verify_master_key)
retrieve_button.grid(row=1, column=1)

tree_retrieve = ttk.Treeview(tab3, columns=("Website", "Username", "Password"))
tree_retrieve.heading("#1", text="Website")
tree_retrieve.heading("#2", text="Username")
tree_retrieve.heading("#3", text="Password")
tree_retrieve.grid(row=2, column=0, columnspan=3)
tree_retrieve.column("#1", width=200)
tree_retrieve.column("#2", width=150)
tree_retrieve.column("#3", width=200)

app.mainloop()

# Close the database connection
conn.close()
