import tkinter as tk
from tkinter import messagebox
import sqlite3

# Database Connection
conn = sqlite3.connect("bank_management.db")
cur = conn.cursor()

# Create Customer Table
cur.execute("""
CREATE TABLE IF NOT EXISTS customer(
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    gender TEXT,
    dob TEXT,
    phone TEXT,
    email TEXT,
    address TEXT,
    aadhar_number TEXT,
    pan_number TEXT
)
""")
conn.commit()


def open_customer_window():

    customer_form = tk.Tk()
    customer_form.title("Customer Management System")
    customer_form.geometry("900x700")

    selected_id = None

    # ---------------- CLEAR ---------------- #

    def clear_fields():
        nonlocal selected_id

        entry_customer_id.delete(0, tk.END)
        entry_first_name.delete(0, tk.END)
        entry_last_name.delete(0, tk.END)
        entry_gender.delete(0, tk.END)
        entry_dob.delete(0, tk.END)
        entry_phone.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_address.delete(0, tk.END)
        entry_aadhar_number.delete(0, tk.END)
        entry_pan_number.delete(0, tk.END)

        selected_id = None

    # ---------------- FETCH ---------------- #

    def fetch_data():

        listbox.delete(0, tk.END)

        cur.execute("SELECT * FROM customer")

        rows = cur.fetchall()

        for row in rows:
            listbox.insert(tk.END, row)

    # ---------------- INSERT ---------------- #

    def submit_data():

        first_name = entry_first_name.get()
        last_name = entry_last_name.get()
        gender = entry_gender.get()
        dob = entry_dob.get()
        phone = entry_phone.get()
        email = entry_email.get()
        address = entry_address.get()
        aadhar_number = entry_aadhar_number.get()
        pan_number = entry_pan_number.get()

        if (
            first_name == "" or
            last_name == "" or
            gender == "" or
            dob == "" or
            phone == "" or
            email == "" or
            address == "" or
            aadhar_number == "" or
            pan_number == ""
        ):
            messagebox.showerror(
                "Error",
                "All fields are required"
            )
            return

        else:

            cur.execute("""
                INSERT INTO customer
                (first_name, last_name, gender, dob, phone, email, address, aadhar_number, pan_number)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                first_name,
                last_name,
                gender,
                dob,
                phone,
                email,
                address,
                aadhar_number,
                pan_number
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

        entry_customer_id.insert(0, data[0])
        entry_first_name.insert(0, data[1])
        entry_last_name.insert(0, data[2])
        entry_gender.insert(0, data[3])
        entry_dob.insert(0, data[4])
        entry_phone.insert(0, data[5])
        entry_email.insert(0, data[6])
        entry_address.insert(0, data[7])
        entry_aadhar_number.insert(0, data[8])
        entry_pan_number.insert(0, data[9])

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
            UPDATE customer
            SET first_name=?,
                last_name=?,
                gender=?,
                dob=?,
                phone=?,
                email=?,
                address=?,
                aadhar_number=?,
                pan_number=?
            WHERE customer_id=?
        """, (
            entry_first_name.get(),
            entry_last_name.get(),
            entry_gender.get(),
            entry_dob.get(),
            entry_phone.get(),
            entry_email.get(),
            entry_address.get(),
            entry_aadhar_number.get(),
            entry_pan_number.get(),
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
                "DELETE FROM customer WHERE customer_id=?",
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

    tk.Label(customer_form, text="Customer ID").pack()
    entry_customer_id = tk.Entry(customer_form, state="readonly")
    entry_customer_id.pack()

    tk.Label(customer_form, text="First Name").pack()
    entry_first_name = tk.Entry(customer_form)
    entry_first_name.pack()

    tk.Label(customer_form, text="Last Name").pack()
    entry_last_name = tk.Entry(customer_form)
    entry_last_name.pack()

    tk.Label(customer_form, text="Gender").pack()
    entry_gender = tk.Entry(customer_form)
    entry_gender.pack()

    tk.Label(customer_form, text="DOB").pack()
    entry_dob = tk.Entry(customer_form)
    entry_dob.pack()

    tk.Label(customer_form, text="Phone").pack()
    entry_phone = tk.Entry(customer_form)
    entry_phone.pack()

    tk.Label(customer_form, text="Email").pack()
    entry_email = tk.Entry(customer_form)
    entry_email.pack()

    tk.Label(customer_form, text="Address").pack()
    entry_address = tk.Entry(customer_form)
    entry_address.pack()

    tk.Label(customer_form, text="Aadhar Number").pack()
    entry_aadhar_number = tk.Entry(customer_form)
    entry_aadhar_number.pack()

    tk.Label(customer_form, text="PAN Number").pack()
    entry_pan_number = tk.Entry(customer_form)
    entry_pan_number.pack()

    tk.Button(customer_form, text="Save", width=15,
              command=submit_data).pack(pady=5)

    tk.Button(customer_form, text="Update", width=15,
              command=update_data).pack(pady=5)

    tk.Button(customer_form, text="Delete", width=15,
              command=delete_data).pack(pady=5)

    tk.Button(customer_form, text="Clear", width=15,
              command=clear_fields).pack(pady=5)

    tk.Label(
        customer_form,
        text="Customer Records"
    ).pack(pady=10)

    listbox = tk.Listbox(
        customer_form,
        width=120,
        height=15
    )
    listbox.pack()

    listbox.bind(
        "<<ListboxSelect>>",
        on_select
    )

    fetch_data()

    customer_form.mainloop()


if __name__ == "__main__":
    open_customer_window()