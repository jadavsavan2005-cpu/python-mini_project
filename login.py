import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib
import dashboard

# ---------------- DATABASE ----------------

conn = sqlite3.connect("bank_management.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS user(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")
conn.commit()

# ---------------- HASH PASSWORD ----------------

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ---------------- RESET DEFAULT ADMIN ----------------
# Delete old admin (plain password or wrong hash)
cur.execute("DELETE FROM user WHERE username=?", ("admin",))

# Create new admin
cur.execute(
    "INSERT INTO user(username,password) VALUES(?,?)",
    ("admin", hash_password("admin123"))
)

conn.commit()

#print("Default Admin")
#print("Username : admin")
#print("Password : admin123")

# ---------------- LOGIN ----------------

def login():

    username = txt_username.get().strip()
    password = txt_password.get().strip()

    if username == "" or password == "":
        messagebox.showerror("Error", "Enter Username and Password")
        return

    cur.execute(
        "SELECT password FROM user WHERE username=?",
        (username,)
    )

    row = cur.fetchone()

    if row is None:
        messagebox.showerror("Error", "Username not found")
        return

    db_password = row[0]

    if db_password == hash_password(password):
        messagebox.showinfo("Success", "Login Successful")
        root.destroy()

        dashboard.open_dashboard()

    else:
        messagebox.showerror("Error", "Invalid Password")

# ---------------- GUI ----------------

root = tk.Tk()
root.title("Bank Management System")
root.geometry("400x300")
root.resizable(False, False)

tk.Label(
    root,
    text="BANK MANAGEMENT SYSTEM",
    font=("Arial",16,"bold")
).pack(pady=20)

tk.Label(root,text="Username").pack()

txt_username = tk.Entry(root,width=30)
txt_username.pack(pady=5)

tk.Label(root,text="Password").pack()

txt_password = tk.Entry(root,show="*",width=30)
txt_password.pack(pady=5)

tk.Button(
    root,
    text="Login",
    width=20,
    bg="green",
    fg="white",
    command=login
).pack(pady=20)

root.mainloop()

conn.close()