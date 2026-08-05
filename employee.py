import tkinter as tk
from tkinter import messagebox
import sqlite3

# Database Connection
conn = sqlite3.connect("bank_management.db")
cur = conn.cursor()

# Create Employee Table
cur.execute("""
CREATE TABLE IF NOT EXISTS employee(
    employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_name TEXT,
    gender TEXT,
    dob TEXT,
    phone TEXT,
    email TEXT,
    address TEXT,
    designation TEXT,
    salary REAL,
    joining_date TEXT
)
""")
conn.commit()


def open_employee_window():

    employee_form = tk.Tk()
    employee_form.title("Employee Management System")
    employee_form.geometry("900x700")

    selected_id = None

    # ---------------- CLEAR ---------------- #

    def clear_fields():
        nonlocal selected_id

        entry_employee_id.config(state="normal")
        entry_employee_id.delete(0, tk.END)
        entry_employee_id.config(state="readonly")

        entry_employee_name.delete(0, tk.END)
        entry_gender.delete(0, tk.END)
        entry_dob.delete(0, tk.END)
        entry_phone.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_address.delete(0, tk.END)
        entry_designation.delete(0, tk.END)
        entry_salary.delete(0, tk.END)
        entry_joining_date.delete(0, tk.END)

        selected_id = None

    # ---------------- FETCH ---------------- #

    def fetch_data():

        listbox.delete(0, tk.END)

        cur.execute("SELECT * FROM employee")

        rows = cur.fetchall()

        for row in rows:
            listbox.insert(tk.END, row)

    # ---------------- INSERT ---------------- #

    def submit_data():

        employee_name = entry_employee_name.get()
        gender = entry_gender.get()
        dob = entry_dob.get()
        phone = entry_phone.get()
        email = entry_email.get()
        address = entry_address.get()
        designation = entry_designation.get()
        salary = entry_salary.get()
        joining_date = entry_joining_date.get()

        if (
            employee_name == "" or
            gender == "" or
            dob == "" or
            phone == "" or
            email == "" or
            address == "" or
            designation == "" or
            salary == "" or
            joining_date == ""
        ):
            messagebox.showerror(
                "Error",
                "All fields are required"
            )
            return

        else:

            cur.execute("""
                INSERT INTO employee
                (employee_name, gender, dob, phone, email, address, designation, salary, joining_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                employee_name,
                gender,
                dob,
                phone,
                email,
                address,
                designation,
                salary,
                joining_date
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

        entry_employee_id.config(state="normal")
        entry_employee_id.insert(0, data[0])
        entry_employee_id.config(state="readonly")

        entry_employee_name.insert(0, data[1])
        entry_gender.insert(0, data[2])
        entry_dob.insert(0, data[3])
        entry_phone.insert(0, data[4])
        entry_email.insert(0, data[5])
        entry_address.insert(0, data[6])
        entry_designation.insert(0, data[7])
        entry_salary.insert(0, data[8])
        entry_joining_date.insert(0, data[9])

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
            UPDATE employee
            SET employee_name=?,
                gender=?,
                dob=?,
                phone=?,
                email=?,
                address=?,
                designation=?,
                salary=?,
                joining_date=?
            WHERE employee_id=?
        """, (
            entry_employee_name.get(),
            entry_gender.get(),
            entry_dob.get(),
            entry_phone.get(),
            entry_email.get(),
            entry_address.get(),
            entry_designation.get(),
            entry_salary.get(),
            entry_joining_date.get(),
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
                "DELETE FROM employee WHERE employee_id=?",
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

    tk.Label(employee_form, text="Employee ID").pack()
    entry_employee_id = tk.Entry(employee_form, state="readonly")
    entry_employee_id.pack()

    tk.Label(employee_form, text="Employee Name").pack()
    entry_employee_name = tk.Entry(employee_form)
    entry_employee_name.pack()

    tk.Label(employee_form, text="Gender").pack()
    entry_gender = tk.Entry(employee_form)
    entry_gender.pack()

    tk.Label(employee_form, text="DOB").pack()
    entry_dob = tk.Entry(employee_form)
    entry_dob.pack()

    tk.Label(employee_form, text="Phone").pack()
    entry_phone = tk.Entry(employee_form)
    entry_phone.pack()

    tk.Label(employee_form, text="Email").pack()
    entry_email = tk.Entry(employee_form)
    entry_email.pack()

    tk.Label(employee_form, text="Address").pack()
    entry_address = tk.Entry(employee_form)
    entry_address.pack()

    tk.Label(employee_form, text="Designation").pack()
    entry_designation = tk.Entry(employee_form)
    entry_designation.pack()

    tk.Label(employee_form, text="Salary").pack()
    entry_salary = tk.Entry(employee_form)
    entry_salary.pack()

    tk.Label(employee_form, text="Joining Date").pack()
    entry_joining_date = tk.Entry(employee_form)
    entry_joining_date.pack()

    tk.Button(employee_form, text="Save", width=15,
              command=submit_data).pack(pady=5)

    tk.Button(employee_form, text="Update", width=15,
              command=update_data).pack(pady=5)

    tk.Button(employee_form, text="Delete", width=15,
              command=delete_data).pack(pady=5)

    tk.Button(employee_form, text="Clear", width=15,
              command=clear_fields).pack(pady=5)

    tk.Label(
        employee_form,
        text="Employee Records"
    ).pack(pady=10)

    listbox = tk.Listbox(
        employee_form,
        width=120,
        height=15
    )
    listbox.pack()

    listbox.bind(
        "<<ListboxSelect>>",
        on_select
    )

    fetch_data()

    employee_form.mainloop()


if __name__ == "__main__":
    open_employee_window()