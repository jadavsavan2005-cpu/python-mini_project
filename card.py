import tkinter as tk
from tkinter import messagebox
import sqlite3

# Database Connection
conn = sqlite3.connect("bank_management.db")
cur = conn.cursor()

# Create Card Table
cur.execute("""
CREATE TABLE IF NOT EXISTS card(
    card_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    account_number TEXT,
    card_number TEXT,
    card_type TEXT,
    issue_date TEXT,
    expiry_date TEXT,
    cvv TEXT,
    card_status TEXT,
    pin TEXT,
    FOREIGN KEY(customer_id) REFERENCES customer(customer_id)
)
""")
conn.commit()


def open_card_window():

    card_form = tk.Tk()
    card_form.title("Card Management System")
    card_form.geometry("900x700")

    selected_id = None

    # ---------------- CLEAR ---------------- #

    def clear_fields():
        nonlocal selected_id

        entry_card_id.config(state="normal")
        entry_card_id.delete(0, tk.END)
        entry_card_id.config(state="readonly")

        entry_customer_id.delete(0, tk.END)
        entry_account_number.delete(0, tk.END)
        entry_card_number.delete(0, tk.END)
        entry_card_type.delete(0, tk.END)
        entry_issue_date.delete(0, tk.END)
        entry_expiry_date.delete(0, tk.END)
        entry_cvv.delete(0, tk.END)
        entry_card_status.delete(0, tk.END)
        entry_pin.delete(0, tk.END)

        selected_id = None

    # ---------------- FETCH ---------------- #

    def fetch_data():

        listbox.delete(0, tk.END)

        cur.execute("SELECT * FROM card")

        rows = cur.fetchall()

        for row in rows:
            listbox.insert(tk.END, row)

    # ---------------- INSERT ---------------- #

    def submit_data():

        customer_id = entry_customer_id.get()
        account_number = entry_account_number.get()
        card_number = entry_card_number.get()
        card_type = entry_card_type.get()
        issue_date = entry_issue_date.get()
        expiry_date = entry_expiry_date.get()
        cvv = entry_cvv.get()
        card_status = entry_card_status.get()
        pin = entry_pin.get()

        if (
            customer_id == "" or
            account_number == "" or
            card_number == "" or
            card_type == "" or
            issue_date == "" or
            expiry_date == "" or
            cvv == "" or
            card_status == "" or
            pin == ""
        ):
            messagebox.showerror(
                "Error",
                "All fields are required"
            )
            return

        else:

            cur.execute("""
                INSERT INTO card
                (customer_id, account_number, card_number, card_type, issue_date, expiry_date, cvv, card_status, pin)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                customer_id,
                account_number,
                card_number,
                card_type,
                issue_date,
                expiry_date,
                cvv,
                card_status,
                pin
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

        entry_card_id.config(state="normal")
        entry_card_id.insert(0, data[0])
        entry_card_id.config(state="readonly")

        entry_customer_id.insert(0, data[1])
        entry_account_number.insert(0, data[2])
        entry_card_number.insert(0, data[3])
        entry_card_type.insert(0, data[4])
        entry_issue_date.insert(0, data[5])
        entry_expiry_date.insert(0, data[6])
        entry_cvv.insert(0, data[7])
        entry_card_status.insert(0, data[8])
        entry_pin.insert(0, data[9])

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
            UPDATE card
            SET customer_id=?,
                account_number=?,
                card_number=?,
                card_type=?,
                issue_date=?,
                expiry_date=?,
                cvv=?,
                card_status=?,
                pin=?
            WHERE card_id=?
        """, (
            entry_customer_id.get(),
            entry_account_number.get(),
            entry_card_number.get(),
            entry_card_type.get(),
            entry_issue_date.get(),
            entry_expiry_date.get(),
            entry_cvv.get(),
            entry_card_status.get(),
            entry_pin.get(),
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
                "DELETE FROM card WHERE card_id=?",
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

    tk.Label(card_form, text="Card ID").pack()
    entry_card_id = tk.Entry(card_form, state="readonly")
    entry_card_id.pack()

    tk.Label(card_form, text="Customer ID").pack()
    entry_customer_id = tk.Entry(card_form)
    entry_customer_id.pack()

    tk.Label(card_form, text="Account Number").pack()
    entry_account_number = tk.Entry(card_form)
    entry_account_number.pack()

    tk.Label(card_form, text="Card Number").pack()
    entry_card_number = tk.Entry(card_form)
    entry_card_number.pack()

    tk.Label(card_form, text="Card Type").pack()
    entry_card_type = tk.Entry(card_form)
    entry_card_type.pack()

    tk.Label(card_form, text="Issue Date").pack()
    entry_issue_date = tk.Entry(card_form)
    entry_issue_date.pack()

    tk.Label(card_form, text="Expiry Date").pack()
    entry_expiry_date = tk.Entry(card_form)
    entry_expiry_date.pack()

    tk.Label(card_form, text="CVV").pack()
    entry_cvv = tk.Entry(card_form)
    entry_cvv.pack()

    tk.Label(card_form, text="Card Status").pack()
    entry_card_status = tk.Entry(card_form)
    entry_card_status.pack()

    tk.Label(card_form, text="PIN").pack()
    entry_pin = tk.Entry(card_form)
    entry_pin.pack()

    tk.Button(card_form, text="Save", width=15,
              command=submit_data).pack(pady=5)

    tk.Button(card_form, text="Update", width=15,
              command=update_data).pack(pady=5)

    tk.Button(card_form, text="Delete", width=15,
              command=delete_data).pack(pady=5)

    tk.Button(card_form, text="Clear", width=15,
              command=clear_fields).pack(pady=5)

    tk.Label(
        card_form,
        text="Card Records"
    ).pack(pady=10)

    listbox = tk.Listbox(
        card_form,
        width=120,
        height=15
    )
    listbox.pack()

    listbox.bind(
        "<<ListboxSelect>>",
        on_select
    )

    fetch_data()

    card_form.mainloop()


if __name__ == "__main__":
    open_card_window()