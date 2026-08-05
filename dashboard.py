import tkinter as tk
from tkinter import messagebox

import customer
import card
import account
import deposit
import withdrawal
import transaction_history
import loan
import employee
import transfer


def open_dashboard():

    dash = tk.Tk()
    dash.title("Bank Management System")
    dash.geometry("1000x650")
    

    # ---------------- Title ----------------

    tk.Label(
        dash,
        text="BANK MANAGEMENT SYSTEM",
        font=("Arial", 24, "bold"),
        pady=15
    ).pack(fill="x")

    tk.Label(
        dash,
        text="Admin Dashboard",
        font=("Arial", 18, "bold"),
    ).pack(pady=20)

    frame = tk.Frame(dash, )
    frame.pack(pady=20)

    # ---------------- Open Functions ----------------

    def open_customer():
        customer.open_customer_window()

    def open_card():
        card.open_card_window()

    def open_account():
        account.open_account_window()

    def open_deposit():
        deposit.open_deposit_window()

    def open_withdraw():
        withdrawal.open_withdrawal_window()

    def open_transaction():
        transaction_history.open_transaction_history_window()

    def open_loan():
        loan.open_loan_window()

    def open_employee():
        employee.open_employee_window()

    def open_transfer():
        transfer.open_transfer_window()


    # ---------------- Buttons ----------------

    tk.Button(frame, text="Customer", width=20, height=2,
              command=open_customer).grid(row=0, column=0, padx=10, pady=10)

    tk.Button(frame, text="Card", width=20, height=2,
              command=open_card).grid(row=0, column=1, padx=10, pady=10)

    tk.Button(frame, text="Account", width=20, height=2,
              command=open_account).grid(row=0, column=2, padx=10, pady=10)

    tk.Button(frame, text="Deposit", width=20, height=2,
              command=open_deposit).grid(row=1, column=0, padx=10, pady=10)

    tk.Button(frame, text="Withdrawal", width=20, height=2,
              command=open_withdraw).grid(row=1, column=1, padx=10, pady=10)

    tk.Button(frame, text="Transaction", width=20, height=2,
              command=open_transaction).grid(row=1, column=2, padx=10, pady=10)

    tk.Button(frame, text="Loan", width=20, height=2,
              command=open_loan).grid(row=2, column=0, padx=10, pady=10)

    tk.Button(frame, text="Employee", width=20, height=2,
              command=open_employee).grid(row=2, column=1, padx=10, pady=10)
    
    tk.Button(frame,text="transfer",width=20,height=2,command=open_transfer).grid(row=2,column=1,padx=10,pady=10)

    dash.mainloop()


if __name__ == "__main__":
    open_dashboard()