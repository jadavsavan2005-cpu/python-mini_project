import tkinter as tk
from tkinter import messagebox
import sqlite3

# Database Connection
conn = sqlite3.connect("bank_management.db")
cur = conn.cursor()

# Create Transaction History Table
cur.execute("""
CREATE TABLE IF NOT EXISTS transaction_history(
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_number TEXT,
    customer_name TEXT,
    transaction_type TEXT,
    amount REAL,
    transaction_date TEXT,
    balance_after REAL,
    payment_mode TEXT,
    remarks TEXT,
    status TEXT
)
""")
conn.commit()


def open_transaction_history_window():

    transaction_history_form = tk.Tk()
    transaction_history_form.title("Transaction History Management System")
    transaction_history_form.geometry("900x700")

    selected_id = None

    # ---------------- CLEAR ---------------- #

    def clear_fields():
        nonlocal selected_id

        entry_transaction_id.config(state="normal")
        entry_transaction_id.delete(0, tk.END)
        entry_transaction_id.config(state="readonly")

        entry_account_number.delete(0, tk.END)
        entry_customer_name.delete(0, tk.END)
        entry_transaction_type.delete(0, tk.END)
        entry_amount.delete(0, tk.END)
        entry_transaction_date.delete(0, tk.END)
        entry_balance_after.delete(0, tk.END)
        entry_payment_mode.delete(0, tk.END)
        entry_remarks.delete(0, tk.END)
        entry_status.delete(0, tk.END)

        selected_id = None

    # ---------------- FETCH ---------------- #

    def fetch_data():

        listbox.delete(0, tk.END)

        cur.execute("SELECT * FROM transaction_history")

        rows = cur.fetchall()

        for row in rows:
            listbox.insert(tk.END, row)

    # ---------------- INSERT ---------------- #

    def submit_data():

        account_number = entry_account_number.get()
        customer_name = entry_customer_name.get()
        transaction_type = entry_transaction_type.get()
        amount = entry_amount.get()
        transaction_date = entry_transaction_date.get()
        balance_after = entry_balance_after.get()
        payment_mode = entry_payment_mode.get()
        remarks = entry_remarks.get()
        status = entry_status.get()

        if (
            account_number == "" or
            customer_name == "" or
            transaction_type == "" or
            amount == "" or
            transaction_date == "" or
            balance_after == "" or
            payment_mode == "" or
            remarks == "" or
            status == ""
        ):
            messagebox.showerror(
                "Error",
                "All fields are required"
            )
            return

        else:

            cur.execute("""
                INSERT INTO transaction_history
                (account_number, customer_name, transaction_type, amount, transaction_date, balance_after, payment_mode, remarks, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                account_number,
                customer_name,
                transaction_type,
                amount,
                transaction_date,
                balance_after,
                payment_mode,
                remarks,
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

        entry_transaction_id.config(state="normal")
        entry_transaction_id.insert(0, data[0])
        entry_transaction_id.config(state="readonly")

        entry_account_number.insert(0, data[1])
        entry_customer_name.insert(0, data[2])
        entry_transaction_type.insert(0, data[3])
        entry_amount.insert(0, data[4])
        entry_transaction_date.insert(0, data[5])
        entry_balance_after.insert(0, data[6])
        entry_payment_mode.insert(0, data[7])
        entry_remarks.insert(0, data[8])
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
            UPDATE transaction_history
            SET account_number=?,
                customer_name=?,
                transaction_type=?,
                amount=?,
                transaction_date=?,
                balance_after=?,
                payment_mode=?,
                remarks=?,
                status=?
            WHERE transaction_id=?
        """, (
            entry_account_number.get(),
            entry_customer_name.get(),
            entry_transaction_type.get(),
            entry_amount.get(),
            entry_transaction_date.get(),
            entry_balance_after.get(),
            entry_payment_mode.get(),
            entry_remarks.get(),
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
                "DELETE FROM transaction_history WHERE transaction_id=?",
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

    tk.Label(transaction_history_form, text="Transaction ID").pack()
    entry_transaction_id = tk.Entry(transaction_history_form, state="readonly")
    entry_transaction_id.pack()

    tk.Label(transaction_history_form, text="Account Number").pack()
    entry_account_number = tk.Entry(transaction_history_form)
    entry_account_number.pack()

    tk.Label(transaction_history_form, text="Customer Name").pack()
    entry_customer_name = tk.Entry(transaction_history_form)
    entry_customer_name.pack()

    tk.Label(transaction_history_form, text="Transaction Type").pack()
    entry_transaction_type = tk.Entry(transaction_history_form)
    entry_transaction_type.pack()

    tk.Label(transaction_history_form, text="Amount").pack()
    entry_amount = tk.Entry(transaction_history_form)
    entry_amount.pack()

    tk.Label(transaction_history_form, text="Transaction Date").pack()
    entry_transaction_date = tk.Entry(transaction_history_form)
    entry_transaction_date.pack()

    tk.Label(transaction_history_form, text="Balance After").pack()
    entry_balance_after = tk.Entry(transaction_history_form)
    entry_balance_after.pack()

    tk.Label(transaction_history_form, text="Payment Mode").pack()
    entry_payment_mode = tk.Entry(transaction_history_form)
    entry_payment_mode.pack()

    tk.Label(transaction_history_form, text="Remarks").pack()
    entry_remarks = tk.Entry(transaction_history_form)
    entry_remarks.pack()

    tk.Label(transaction_history_form, text="Status").pack()
    entry_status = tk.Entry(transaction_history_form)
    entry_status.pack()

    tk.Button(transaction_history_form, text="Save", width=15,
              command=submit_data).pack(pady=5)

    tk.Button(transaction_history_form, text="Update", width=15,
              command=update_data).pack(pady=5)

    tk.Button(transaction_history_form, text="Delete", width=15,
              command=delete_data).pack(pady=5)

    tk.Button(transaction_history_form, text="Clear", width=15,
              command=clear_fields).pack(pady=5)

    tk.Label(
        transaction_history_form,
        text="Transaction History Records"
    ).pack(pady=10)

    listbox = tk.Listbox(
        transaction_history_form,
        width=100,
        height=15
    )
    listbox.pack()

    listbox.bind(
        "<<ListboxSelect>>",
        on_select
    )

    fetch_data()

    transaction_history_form.mainloop()


if __name__ == "__main__":
    open_transaction_history_window()