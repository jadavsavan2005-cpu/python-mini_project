import tkinter as tk
from tkinter import messagebox
import sqlite3

# Database Connection
conn = sqlite3.connect("bank_management.db")
cur = conn.cursor()

# Create Transfer Table
cur.execute("""
CREATE TABLE IF NOT EXISTS transfer(
    transfer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_account TEXT,
    receiver_account TEXT,
    sender_name TEXT,
    receiver_name TEXT,
    amount REAL,
    transfer_date TEXT,
    transaction_id TEXT,
    remarks TEXT,
    status TEXT
)
""")
conn.commit()


def open_transfer_window():

    transfer_form = tk.Tk()
    transfer_form.title("Transfer Management System")
    transfer_form.geometry("900x700")

    selected_id = None

    # ---------------- CLEAR ---------------- #

    def clear_fields():
        nonlocal selected_id

        entry_transfer_id.config(state="normal")
        entry_transfer_id.delete(0, tk.END)
        entry_transfer_id.config(state="readonly")

        entry_sender_account.delete(0, tk.END)
        entry_receiver_account.delete(0, tk.END)
        entry_sender_name.delete(0, tk.END)
        entry_receiver_name.delete(0, tk.END)
        entry_amount.delete(0, tk.END)
        entry_transfer_date.delete(0, tk.END)
        entry_transaction_id.delete(0, tk.END)
        entry_remarks.delete(0, tk.END)
        entry_status.delete(0, tk.END)

        selected_id = None

    # ---------------- FETCH ---------------- #

    def fetch_data():

        listbox.delete(0, tk.END)

        cur.execute("SELECT * FROM transfer")

        rows = cur.fetchall()

        for row in rows:
            listbox.insert(tk.END, row)

    # ---------------- INSERT ---------------- #

    def submit_data():

        sender_account = entry_sender_account.get()
        receiver_account = entry_receiver_account.get()
        sender_name = entry_sender_name.get()
        receiver_name = entry_receiver_name.get()
        amount = entry_amount.get()
        transfer_date = entry_transfer_date.get()
        transaction_id = entry_transaction_id.get()
        remarks = entry_remarks.get()
        status = entry_status.get()

        if (
            sender_account == "" or
            receiver_account == "" or
            sender_name == "" or
            receiver_name == "" or
            amount == "" or
            transfer_date == "" or
            transaction_id == "" or
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
                INSERT INTO transfer
                (sender_account, receiver_account, sender_name, receiver_name, amount, transfer_date, transaction_id, remarks, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                sender_account,
                receiver_account,
                sender_name,
                receiver_name,
                amount,
                transfer_date,
                transaction_id,
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

        entry_transfer_id.config(state="normal")
        entry_transfer_id.insert(0, data[0])
        entry_transfer_id.config(state="readonly")

        entry_sender_account.insert(0, data[1])
        entry_receiver_account.insert(0, data[2])
        entry_sender_name.insert(0, data[3])
        entry_receiver_name.insert(0, data[4])
        entry_amount.insert(0, data[5])
        entry_transfer_date.insert(0, data[6])
        entry_transaction_id.insert(0, data[7])
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
            UPDATE transfer
            SET sender_account=?,
                receiver_account=?,
                sender_name=?,
                receiver_name=?,
                amount=?,
                transfer_date=?,
                transaction_id=?,
                remarks=?,
                status=?
            WHERE transfer_id=?
        """, (
            entry_sender_account.get(),
            entry_receiver_account.get(),
            entry_sender_name.get(),
            entry_receiver_name.get(),
            entry_amount.get(),
            entry_transfer_date.get(),
            entry_transaction_id.get(),
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
                "DELETE FROM transfer WHERE transfer_id=?",
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

    tk.Label(transfer_form, text="Transfer ID").pack()
    entry_transfer_id = tk.Entry(transfer_form, state="readonly")
    entry_transfer_id.pack()

    tk.Label(transfer_form, text="Sender Account").pack()
    entry_sender_account = tk.Entry(transfer_form)
    entry_sender_account.pack()

    tk.Label(transfer_form, text="Receiver Account").pack()
    entry_receiver_account = tk.Entry(transfer_form)
    entry_receiver_account.pack()

    tk.Label(transfer_form, text="Sender Name").pack()
    entry_sender_name = tk.Entry(transfer_form)
    entry_sender_name.pack()

    tk.Label(transfer_form, text="Receiver Name").pack()
    entry_receiver_name = tk.Entry(transfer_form)
    entry_receiver_name.pack()

    tk.Label(transfer_form, text="Amount").pack()
    entry_amount = tk.Entry(transfer_form)
    entry_amount.pack()

    tk.Label(transfer_form, text="Transfer Date").pack()
    entry_transfer_date = tk.Entry(transfer_form)
    entry_transfer_date.pack()

    tk.Label(transfer_form, text="Transaction ID").pack()
    entry_transaction_id = tk.Entry(transfer_form)
    entry_transaction_id.pack()

    tk.Label(transfer_form, text="Remarks").pack()
    entry_remarks = tk.Entry(transfer_form)
    entry_remarks.pack()

    tk.Label(transfer_form, text="Status").pack()
    entry_status = tk.Entry(transfer_form)
    entry_status.pack()

    tk.Button(transfer_form, text="Save", width=15,
              command=submit_data).pack(pady=5)

    tk.Button(transfer_form, text="Update", width=15,
              command=update_data).pack(pady=5)

    tk.Button(transfer_form, text="Delete", width=15,
              command=delete_data).pack(pady=5)

    tk.Button(transfer_form, text="Clear", width=15,
              command=clear_fields).pack(pady=5)

    tk.Label(
        transfer_form,
        text="Transfer Records"
    ).pack(pady=10)

    listbox = tk.Listbox(
        transfer_form,
        width=120,
        height=15
    )
    listbox.pack()

    listbox.bind(
        "<<ListboxSelect>>",
        on_select
    )

    fetch_data()

    transfer_form.mainloop()


if __name__ == "__main__":
    open_transfer_window()