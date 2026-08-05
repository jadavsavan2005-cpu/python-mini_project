import sqlite3

# Connect Database
conn = sqlite3.connect("bank_management.db")
cursor = conn.cursor()


# 2. Customer Table
cursor.execute("""
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

# 3. Account Table
cursor.execute("""
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

# 4. Employee Table
cursor.execute("""
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

# 5. Deposit Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS deposit(
    deposit_id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_number TEXT,
    customer_name TEXT,
    amount REAL,
    deposit_date TEXT,
    payment_mode TEXT,
    transaction_id TEXT,
    remarks TEXT,
    employee_name TEXT,
    status TEXT
)
""")

# 6. Withdrawal Table
cursor.execute("""
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

# 7. Transfer Table
cursor.execute("""
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

# 8. Loan Table
cursor.execute("""
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

# 9. Card Table
cursor.execute("""
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

# 10. Transaction Table
cursor.execute("""
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
#user table
cursor.execute("""
CREATE TABLE IF NOT EXISTS user(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

conn.commit()
conn.close()

print("===================================")
print("Bank Management Database Created")
print("Database Name : bank_management.db")
