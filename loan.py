import tkinter as tk
from tkinter import messagebox
import sqlite3

# Database Connection
conn = sqlite3.connect("bank_management.db")
cur = conn.cursor()

# Create Loan Table
cur.execute("""
CREATE TABLE IF NOT EXISTS loan(
    loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    loan_type TEXT,
    loan_amount REAL,
    interest_rate REAL,
    loan_date TEXT,
    duration_months INTEGER,
    emi_amount REAL,
    status TEXT,
    approved_by TEXT,
    FOREIGN KEY(customer_id) REFERENCES customer(customer_id)
)
""")
conn.commit()


def open_loan_window():

    loan_form = tk.Tk()
    loan_form.title("Loan Management System")
    loan_form.geometry("900x700")

    selected_id = None

    # ---------------- CLEAR ---------------- #

    def clear_fields():
        nonlocal selected_id

        entry_loan_id.config(state="normal")
        entry_loan_id.delete(0, tk.END)
        entry_loan_id.config(state="readonly")

        entry_customer_id.delete(0, tk.END)
        entry_loan_type.delete(0, tk.END)
        entry_loan_amount.delete(0, tk.END)
        entry_interest_rate.delete(0, tk.END)
        entry_loan_date.delete(0, tk.END)
        entry_duration_months.delete(0, tk.END)
        entry_emi_amount.delete(0, tk.END)
        entry_status.delete(0, tk.END)
        entry_approved_by.delete(0, tk.END)

        selected_id = None

    # ---------------- FETCH ---------------- #

    def fetch_data():

        listbox.delete(0, tk.END)

        cur.execute("SELECT * FROM loan")

        rows = cur.fetchall()

        for row in rows:
            listbox.insert(tk.END, row)

    # ---------------- INSERT ---------------- #

    def submit_data():

        customer_id = entry_customer_id.get()
        loan_type = entry_loan_type.get()
        loan_amount = entry_loan_amount.get()
        interest_rate = entry_interest_rate.get()
        loan_date = entry_loan_date.get()
        duration_months = entry_duration_months.get()
        emi_amount = entry_emi_amount.get()
        status = entry_status.get()
        approved_by = entry_approved_by.get()

        if (
            customer_id == "" or
            loan_type == "" or
            loan_amount == "" or
            interest_rate == "" or
            loan_date == "" or
            duration_months == "" or
            emi_amount == "" or
            status == "" or
            approved_by == ""
        ):
            messagebox.showerror(
                "Error",
                "All fields are required"
            )
            return

        else:

            cur.execute("""
                INSERT INTO loan
                (customer_id, loan_type, loan_amount, interest_rate, loan_date, duration_months, emi_amount, status, approved_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                customer_id,
                loan_type,
                loan_amount,
                interest_rate,
                loan_date,
                duration_months,
                emi_amount,
                status,
                approved_by
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

        entry_loan_id.config(state="normal")
        entry_loan_id.insert(0, data[0])
        entry_loan_id.config(state="readonly")

        entry_customer_id.insert(0, data[1])
        entry_loan_type.insert(0, data[2])
        entry_loan_amount.insert(0, data[3])
        entry_interest_rate.insert(0, data[4])
        entry_loan_date.insert(0, data[5])
        entry_duration_months.insert(0, data[6])
        entry_emi_amount.insert(0, data[7])
        entry_status.insert(0, data[8])
        entry_approved_by.insert(0, data[9])

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
            UPDATE loan
            SET customer_id=?,
                loan_type=?,
                loan_amount=?,
                interest_rate=?,
                loan_date=?,
                duration_months=?,
                emi_amount=?,
                status=?,
                approved_by=?
            WHERE loan_id=?
        """, (
            entry_customer_id.get(),
            entry_loan_type.get(),
            entry_loan_amount.get(),
            entry_interest_rate.get(),
            entry_loan_date.get(),
            entry_duration_months.get(),
            entry_emi_amount.get(),
            entry_status.get(),
            entry_approved_by.get(),
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
                "DELETE FROM loan WHERE loan_id=?",
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

    tk.Label(loan_form, text="Loan ID").pack()
    entry_loan_id = tk.Entry(loan_form, state="readonly")
    entry_loan_id.pack()

    tk.Label(loan_form, text="Customer ID").pack()
    entry_customer_id = tk.Entry(loan_form)
    entry_customer_id.pack()

    tk.Label(loan_form, text="Loan Type").pack()
    entry_loan_type = tk.Entry(loan_form)
    entry_loan_type.pack()

    tk.Label(loan_form, text="Loan Amount").pack()
    entry_loan_amount = tk.Entry(loan_form)
    entry_loan_amount.pack()

    tk.Label(loan_form, text="Interest Rate").pack()
    entry_interest_rate = tk.Entry(loan_form)
    entry_interest_rate.pack()

    tk.Label(loan_form, text="Loan Date").pack()
    entry_loan_date = tk.Entry(loan_form)
    entry_loan_date.pack()

    tk.Label(loan_form, text="Duration (Months)").pack()
    entry_duration_months = tk.Entry(loan_form)
    entry_duration_months.pack()

    tk.Label(loan_form, text="EMI Amount").pack()
    entry_emi_amount = tk.Entry(loan_form)
    entry_emi_amount.pack()

    tk.Label(loan_form, text="Status").pack()
    entry_status = tk.Entry(loan_form)
    entry_status.pack()

    tk.Label(loan_form, text="Approved By").pack()
    entry_approved_by = tk.Entry(loan_form)
    entry_approved_by.pack()

    tk.Button(loan_form, text="Save", width=15,
              command=submit_data).pack(pady=5)

    tk.Button(loan_form, text="Update", width=15,
              command=update_data).pack(pady=5)

    tk.Button(loan_form, text="Delete", width=15,
              command=delete_data).pack(pady=5)

    tk.Button(loan_form, text="Clear", width=15,
              command=clear_fields).pack(pady=5)

    tk.Label(
        loan_form,
        text="Loan Records"
    ).pack(pady=10)

    listbox = tk.Listbox(
        loan_form,
        width=120,
        height=15
    )
    listbox.pack()

    listbox.bind(
        "<<ListboxSelect>>",
        on_select
    )

    fetch_data()

    loan_form.mainloop()


if __name__ == "__main__":
    open_loan_window()