import sqlite3

def create_database():
    conn = sqlite3.connect('bank_management.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            accNo INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            deposit INTEGER NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            accNo INTEGER NOT NULL,
            txn_date TEXT NOT NULL,
            txn_type TEXT NOT NULL,
            amount INTEGER NOT NULL,
            FOREIGN KEY (accNo) REFERENCES accounts(accNo)
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
