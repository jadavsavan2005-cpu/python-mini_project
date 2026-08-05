import tkinter as tk
from tkinter import messagebox
import sqlite3

# Database Connection
conn = sqlite3.connect("bank_management.db")
cur = conn.cursor()

# Create Account Table
cur.execute("""
CREATE TABLE IF NOT EXISTS account(
    account_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    account_number TEXT UNIQUE,
    account_type TEXT,
    balance REAL,
    branch_name TEXT,
    ifsc_code TEXT,
    open_date TEXT,
    status TEXT,
    nominee_name TEXT,
    FOREIGN KEY(customer_id) REFERENCES customer(customer_id)
)
""")
conn.commit()


def open_account_window():

    account_form = tk.Tk()
    account_form.title("Account Management System")
    account_form.geometry("900x700")

    selected_id = None

    # ---------------- CLEAR ---------------- #

    def clear_fields():
        nonlocal selected_id

        entry_account_id.config(state="normal")
        entry_account_id.delete(0, tk.END)
        entry_account_id.config(state="readonly")

        entry_customer_id.delete(0, tk.END)
        entry_account_number.delete(0, tk.END)
        entry_account_type.delete(0, tk.END)
        entry_balance.delete(0, tk.END)
        entry_branch_name.delete(0, tk.END)
        entry_ifsc_code.delete(0, tk.END)
        entry_open_date.delete(0, tk.END)
        entry_status.delete(0, tk.END)
        entry_nominee_name.delete(0, tk.END)

        selected_id = None

    # ---------------- FETCH ---------------- #

    def fetch_data():

        listbox.delete(0, tk.END)

        cur.execute("SELECT * FROM account")

        rows = cur.fetchall()

        for row in rows:
            listbox.insert(tk.END, row)

    # ---------------- INSERT ---------------- #

    def submit_data():

        customer_id = entry_customer_id.get()
        account_number = entry_account_number.get()
        account_type = entry_account_type.get()
        balance = entry_balance.get()
        branch_name = entry_branch_name.get()
        ifsc_code = entry_ifsc_code.get()
        open_date = entry_open_date.get()
        status = entry_status.get()
        nominee_name = entry_nominee_name.get()

        if (
            customer_id == "" or
            account_number == "" or
            account_type == "" or
            balance == "" or
            branch_name == "" or
            ifsc_code == "" or
            open_date == "" or
            status == "" or
            nominee_name == ""
        ):
            messagebox.showerror(
                "Error",
                "All fields are required"
            )
            return

        else:

           
                cur.execute("""
                    INSERT INTO account
                    (customer_id, account_number, account_type, balance, branch_name, ifsc_code, open_date, status, nominee_name)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    customer_id,
                    account_number,
                    account_type,
                    balance,
                    branch_name,
                    ifsc_code,
                    open_date,
                    status,
                    nominee_name
                ))

                conn.commit()

                fetch_data()
                clear_fields()

                messagebox.showinfo(
                    "Success",
                    "Record inserted Successfully"
                )

            

    # ---------------- SELECT ---------------- #

    def on_select(event):

        nonlocal selected_id

        selected = listbox.curselection()

        if not selected:
            return

        data = listbox.get(selected[0])

        clear_fields()

        selected_id = data[0]

        entry_account_id.config(state="normal")
        entry_account_id.insert(0, data[0])
        entry_account_id.config(state="readonly")

        entry_customer_id.insert(0, data[1])
        entry_account_number.insert(0, data[2])
        entry_account_type.insert(0, data[3])
        entry_balance.insert(0, data[4])
        entry_branch_name.insert(0, data[5])
        entry_ifsc_code.insert(0, data[6])
        entry_open_date.insert(0, data[7])
        entry_status.insert(0, data[8])
        entry_nominee_name.insert(0, data[9])

    # ---------------- UPDATE ---------------- #

    def update_data():

        nonlocal selected_id

        if selected_id is None:
            messagebox.showerror(
                "Error",
                "Select a record first"
            )
            return

        else:
            cur.execute("""
                UPDATE account
                SET customer_id=?,
                    account_number=?,
                    account_type=?,
                    balance=?,
                    branch_name=?,
                    ifsc_code=?,
                    open_date=?,
                    status=?,
                    nominee_name=?
                WHERE account_id=?
            """, (
                entry_customer_id.get(),
                entry_account_number.get(),
                entry_account_type.get(),
                entry_balance.get(),
                entry_branch_name.get(),
                entry_ifsc_code.get(),
                entry_open_date.get(),
                entry_status.get(),
                entry_nominee_name.get(),
                selected_id
            ))

            conn.commit()

            fetch_data()
            clear_fields()

            messagebox.showinfo("Success", "Record Updated Successfully")

      
    # ---------------- DELETE ---------------- #

    def delete_data():

        nonlocal selected_id

        if selected_id is None:
            messagebox.showerror(
                "Error",
                "Select a record first"
            )
            return

        answer = messagebox.askyesno(
            "Confirm",
            "Delete selected record?"
        )

        if answer:

            cur.execute(
                "DELETE FROM account WHERE account_id=?",
                (selected_id,)
            )

            conn.commit()

            fetch_data()
            clear_fields()

            messagebox.showinfo(
                "Success",
                "Record Deleted Successfully"
            )

    # ---------------- FORM ---------------- #

    tk.Label(account_form, text="Account ID").pack()
    entry_account_id = tk.Entry(account_form, state="readonly")
    entry_account_id.pack()

    tk.Label(account_form, text="Customer ID").pack()
    entry_customer_id = tk.Entry(account_form)
    entry_customer_id.pack()

    tk.Label(account_form, text="Account Number").pack()
    entry_account_number = tk.Entry(account_form)
    entry_account_number.pack()

    tk.Label(account_form, text="Account Type").pack()
    entry_account_type = tk.Entry(account_form)
    entry_account_type.pack()

    tk.Label(account_form, text="Balance").pack()
    entry_balance = tk.Entry(account_form)
    entry_balance.pack()

    tk.Label(account_form, text="Branch Name").pack()
    entry_branch_name = tk.Entry(account_form)
    entry_branch_name.pack()

    tk.Label(account_form, text="IFSC Code").pack()
    entry_ifsc_code = tk.Entry(account_form)
    entry_ifsc_code.pack()

    tk.Label(account_form, text="Open Date").pack()
    entry_open_date = tk.Entry(account_form)
    entry_open_date.pack()

    tk.Label(account_form, text="Status").pack()
    entry_status = tk.Entry(account_form)
    entry_status.pack()

    tk.Label(account_form, text="Nominee Name").pack()
    entry_nominee_name = tk.Entry(account_form)
    entry_nominee_name.pack()

    tk.Button(account_form, text="Save", width=15,
              command=submit_data).pack(pady=5)

    tk.Button(account_form, text="Update", width=15,
              command=update_data).pack(pady=5)

    tk.Button(account_form, text="Delete", width=15,
              command=delete_data).pack(pady=5)

    tk.Button(account_form, text="Clear", width=15,
              command=clear_fields).pack(pady=5)

    tk.Label(
        account_form,
        text="Account Records"
    ).pack(pady=10)

    listbox = tk.Listbox(
        account_form,
        width=120,
        height=15
    )
    listbox.pack()

    listbox.bind(
        "<<ListboxSelect>>",
        on_select
    )

    fetch_data()

    account_form.mainloop()


if __name__ == "__main__":
    open_account_window()