import tkinter as tk
from tkinter import messagebox
import sqlite3

# Database Connection
conn = sqlite3.connect("bank_management.db")
cur = conn.cursor()

# Create Withdrawal Table
cur.execute("""
CREATE TABLE IF NOT EXISTS withdrawal(
    withdrawal_id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_number TEXT,
    customer_name TEXT,
    amount REAL,
    withdrawal_date TEXT,
    payment_mode TEXT,
    transaction_id TEXT,
    remarks TEXT,
    employee_name TEXT,
    status TEXT
)
""")
conn.commit()


def open_withdrawal_window():

    withdrawal_form = tk.Tk()
    withdrawal_form.title("Withdrawal Management System")
    withdrawal_form.geometry("900x700")

    selected_id = None

    # ---------------- CLEAR ---------------- #

    def clear_fields():
        nonlocal selected_id

        entry_withdrawal_id.config(state="normal")
        entry_withdrawal_id.delete(0, tk.END)
        entry_withdrawal_id.config(state="readonly")

        entry_account_number.delete(0, tk.END)
        entry_customer_name.delete(0, tk.END)
        entry_amount.delete(0, tk.END)
        entry_withdrawal_date.delete(0, tk.END)
        entry_payment_mode.delete(0, tk.END)
        entry_transaction_id.delete(0, tk.END)
        entry_remarks.delete(0, tk.END)
        entry_employee_name.delete(0, tk.END)
        entry_status.delete(0, tk.END)

        selected_id = None

    # ---------------- FETCH ---------------- #

    def fetch_data():

        listbox.delete(0, tk.END)

        cur.execute("SELECT * FROM withdrawal")

        rows = cur.fetchall()

        for row in rows:
            listbox.insert(tk.END, row)

    # ---------------- INSERT ---------------- #

    def submit_data():

        account_number = entry_account_number.get()
        customer_name = entry_customer_name.get()
        amount = entry_amount.get()
        withdrawal_date = entry_withdrawal_date.get()
        payment_mode = entry_payment_mode.get()
        transaction_id = entry_transaction_id.get()
        remarks = entry_remarks.get()
        employee_name = entry_employee_name.get()
        status = entry_status.get()

        if (
            account_number == "" or
            customer_name == "" or
            amount == "" or
            withdrawal_date == "" or
            payment_mode == "" or
            transaction_id == "" or
            remarks == "" or
            employee_name == "" or
            status == ""
        ):
            messagebox.showerror(
                "Error",
                "All fields are required"
            )
            return

        else:

            cur.execute("""
                INSERT INTO withdrawal
                (account_number, customer_name, amount, withdrawal_date, payment_mode, transaction_id, remarks, employee_name, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                account_number,
                customer_name,
                amount,
                withdrawal_date,
                payment_mode,
                transaction_id,
                remarks,
                employee_name,
                status
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

        entry_withdrawal_id.config(state="normal")
        entry_withdrawal_id.insert(0, data[0])
        entry_withdrawal_id.config(state="readonly")

        entry_account_number.insert(0, data[1])
        entry_customer_name.insert(0, data[2])
        entry_amount.insert(0, data[3])
        entry_withdrawal_date.insert(0, data[4])
        entry_payment_mode.insert(0, data[5])
        entry_transaction_id.insert(0, data[6])
        entry_remarks.insert(0, data[7])
        entry_employee_name.insert(0, data[8])
        entry_status.insert(0, data[9])

    # ---------------- UPDATE ---------------- #

    def update_data():

        nonlocal selected_id

        if selected_id is None:
            messagebox.showerror(
                "Error",
                "Select a record first"
            )
            return

        cur.execute("""
            UPDATE withdrawal
            SET account_number=?,
                customer_name=?,
                amount=?,
                withdrawal_date=?,
                payment_mode=?,
                transaction_id=?,
                remarks=?,
                employee_name=?,
                status=?
            WHERE withdrawal_id=?
        """, (
            entry_account_number.get(),
            entry_customer_name.get(),
            entry_amount.get(),
            entry_withdrawal_date.get(),
            entry_payment_mode.get(),
            entry_transaction_id.get(),
            entry_remarks.get(),
            entry_employee_name.get(),
            entry_status.get(),
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
                "DELETE FROM withdrawal WHERE withdrawal_id=?",
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

    tk.Label(withdrawal_form, text="Withdrawal ID").pack()
    entry_withdrawal_id = tk.Entry(withdrawal_form, state="readonly")
    entry_withdrawal_id.pack()

    tk.Label(withdrawal_form, text="Account Number").pack()
    entry_account_number = tk.Entry(withdrawal_form)
    entry_account_number.pack()

    tk.Label(withdrawal_form, text="Customer Name").pack()
    entry_customer_name = tk.Entry(withdrawal_form)
    entry_customer_name.pack()

    tk.Label(withdrawal_form, text="Amount").pack()
    entry_amount = tk.Entry(withdrawal_form)
    entry_amount.pack()

    tk.Label(withdrawal_form, text="Withdrawal Date").pack()
    entry_withdrawal_date = tk.Entry(withdrawal_form)
    entry_withdrawal_date.pack()

    tk.Label(withdrawal_form, text="Payment Mode").pack()
    entry_payment_mode = tk.Entry(withdrawal_form)
    entry_payment_mode.pack()

    tk.Label(withdrawal_form, text="Transaction ID").pack()
    entry_transaction_id = tk.Entry(withdrawal_form)
    entry_transaction_id.pack()

    tk.Label(withdrawal_form, text="Remarks").pack()
    entry_remarks = tk.Entry(withdrawal_form)
    entry_remarks.pack()

    tk.Label(withdrawal_form, text="Employee Name").pack()
    entry_employee_name = tk.Entry(withdrawal_form)
    entry_employee_name.pack()

    tk.Label(withdrawal_form, text="Status").pack()
    entry_status = tk.Entry(withdrawal_form)
    entry_status.pack()

    tk.Button(withdrawal_form, text="Save", width=15,
              command=submit_data).pack(pady=5)

    tk.Button(withdrawal_form, text="Update", width=15,
              command=update_data).pack(pady=5)

    tk.Button(withdrawal_form, text="Delete", width=15,
              command=delete_data).pack(pady=5)

    tk.Button(withdrawal_form, text="Clear", width=15,
              command=clear_fields).pack(pady=5)

    tk.Label(
        withdrawal_form,
        text="Withdrawal Records"
    ).pack(pady=10)

    listbox = tk.Listbox(
        withdrawal_form,
        width=120,
        height=15
    )
    listbox.pack()

    listbox.bind(
        "<<ListboxSelect>>",
        on_select
    )

    fetch_data()

    withdrawal_form.mainloop()


if __name__ == "__main__":
    open_withdrawal_window()