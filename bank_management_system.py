import sqlite3
from datetime import datetime

class Account:
    def __init__(self, accNo=0, name='', deposit=0, type=''):
        self.accNo = accNo
        self.name = name
        self.deposit = deposit
        self.type = type

    def generate_account_number(self):
        conn = sqlite3.connect('bank_management.db')
        cursor = conn.cursor()
        cursor.execute('SELECT MAX(accNo) FROM accounts')
        max_accNo = cursor.fetchone()[0]
        conn.close()
        return (max_accNo or 0) + 1

    def createAccount(self):
        self.accNo = self.generate_account_number()
        self.name = input("Enter the account holder name : ")
        self.type = input("Enter the type of account [C/S] : ").upper()
        while self.type not in ['C', 'S']:
            print("Invalid account type. Please enter 'C' for Current or 'S' for Savings.")
            self.type = input("Enter the type of account [C/S] : ").upper()
        self.deposit = int(input("Enter The Initial amount (>=500 for Saving and >=1000 for Current): "))
        while (self.type == 'S' and self.deposit < 500) or (self.type == 'C' and self.deposit < 1000):
            print("Initial deposit amount is insufficient.")
            self.deposit = int(input("Enter The Initial amount (>=500 for Saving and >=1000 for Current): "))
        self.save_to_db()
        print(f"\n\n\nAccount Created. Your account number is {self.accNo}")

    def save_to_db(self):
        conn = sqlite3.connect('bank_management.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO accounts (accNo, name, type, deposit)
            VALUES (?, ?, ?, ?)
        ''', (self.accNo, self.name, self.type, self.deposit))
        conn.commit()
        conn.close()

    def showAccount(self):
        print("Account Number : ", self.accNo)
        print("Account Holder Name : ", self.name)
        print("Type of Account : ", self.type)
        print("Balance : ", self.deposit)

    def modifyAccount(self):
        print("Account Number : ", self.accNo)
        self.name = input("Modify Account Holder Name : ")
        self.type = input("Modify type of Account : ").upper()
        while self.type not in ['C', 'S']:
            print("Invalid account type. Please enter 'C' for Current or 'S' for Savings.")
            self.type = input("Modify type of Account : ").upper()
        self.deposit = int(input("Modify Balance : "))
        self.update_db()

    def update_db(self):
        conn = sqlite3.connect('bank_management.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE accounts
            SET name = ?, type = ?, deposit = ?
            WHERE accNo = ?
        ''', (self.name, self.type, self.deposit, self.accNo))
        conn.commit()
        conn.close()

    def depositAmount(self, amount):
        self.deposit += amount
        self.update_db()
        self.record_transaction('Deposit', amount)

    def withdrawAmount(self, amount):
        if amount <= self.deposit:
            self.deposit -= amount
            self.update_db()
            self.record_transaction('Withdraw', amount)
        else:
            print("Insufficient funds!")

    def record_transaction(self, txn_type, amount):
        conn = sqlite3.connect('bank_management.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO transactions (accNo, txn_date, txn_type, amount)
            VALUES (?, ?, ?, ?)
        ''', (self.accNo, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), txn_type, amount))
        conn.commit()
        conn.close()

    def apply_interest(self):
        if self.type == 'S':  
            interest_rate = 0.04  
            self.deposit += self.deposit * interest_rate
            self.update_db()
            print(f"Interest applied. New balance is {self.deposit}")

def intro():
    print("\t\t\t\t**********************")
    print("\t\t\t\tBANK MANAGEMENT SYSTEM")
    print("\t\t\t\t**********************")
    input()

def displayAll():
    conn = sqlite3.connect('bank_management.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM accounts')
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            print(f"Account Number: {row[0]}, Name: {row[1]}, Type: {row[2]}, Deposit: {row[3]}")
    else:
        print("No records to display")
    conn.close()

def displaySp(num):
    conn = sqlite3.connect('bank_management.db')
    cursor = conn.cursor()
    cursor.execute('SELECT deposit FROM accounts WHERE accNo = ?', (num,))
    row = cursor.fetchone()
    if row:
        print("Your account Balance is = ", row[0])
    else:
        print("No existing record with this number")
    conn.close()

def depositAndWithdraw(num1, num2):
    conn = sqlite3.connect('bank_management.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM accounts WHERE accNo = ?', (num1,))
    row = cursor.fetchone()
    if row:
        account = Account(*row)
        if num2 == 1:
            amount = int(input("Enter the amount to deposit : "))
            account.depositAmount(amount)
            print("Your account is updated")
        elif num2 == 2:
            amount = int(input("Enter the amount to withdraw : "))
            account.withdrawAmount(amount)
    else:
        print("No records to Search")
    conn.close()

def deleteAccount(num):
    conn = sqlite3.connect('bank_management.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM accounts WHERE accNo = ?', (num,))
    conn.commit()
    conn.close()

def modifyAccount(num):
    conn = sqlite3.connect('bank_management.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM accounts WHERE accNo = ?', (num,))
    row = cursor.fetchone()
    if row:
        account = Account(*row)
        account.modifyAccount()
    else:
        print("No existing record with this number")
    conn.close()

def searchAccountsByName(name):
    conn = sqlite3.connect('bank_management.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM accounts WHERE name LIKE ?', ('%' + name + '%',))
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            print(f"Account Number: {row[0]}, Name: {row[1]}, Type: {row[2]}, Deposit: {row[3]}")
    else:
        print("No accounts found with this name")
    conn.close()

def generateReport():
    conn = sqlite3.connect('bank_management.db')
    cursor = conn.cursor()
    cursor.execute('SELECT type, COUNT(*), SUM(deposit) FROM accounts GROUP BY type')
    rows = cursor.fetchall()
    print("Account Type | Number of Accounts | Total Deposit")
    print("-------------------------------------------------")
    for row in rows:
        print(f"{row[0]}         | {row[1]}                   | {row[2]}")
    conn.close()

# Start of the program
def main():
    intro()
    while True:
        print("\tMAIN MENU")
        print("\t1. NEW ACCOUNT")
        print("\t2. DEPOSIT AMOUNT")
        print("\t3. WITHDRAW AMOUNT")
        print("\t4. BALANCE ENQUIRY")
        print("\t5. ALL ACCOUNT HOLDER LIST")
        print("\t6. CLOSE AN ACCOUNT")
        print("\t7. MODIFY AN ACCOUNT")
        print("\t8. SEARCH ACCOUNTS BY NAME")
        print("\t9. APPLY INTEREST")
        print("\t10. GENERATE REPORT")
        print("\t11. EXIT")
        ch = input("\tSelect Your Option (1-11) ")

        if ch == '1':
            account = Account()
            account.createAccount()
        elif ch == '2':
            num = int(input("\tEnter The account No. : "))
            depositAndWithdraw(num, 1)
        elif ch == '3':
            num = int(input("\tEnter The account No. : "))
            depositAndWithdraw(num, 2)
        elif ch == '4':
            num = int(input("\tEnter The account No. : "))
            displaySp(num)
        elif ch == '5':
            displayAll()
        elif ch == '6':
            num = int(input("\tEnter The account No. : "))
            deleteAccount(num)
        elif ch == '7':
            num = int(input("\tEnter The account No. : "))
            modifyAccount(num)
        elif ch == '8':
            name = input("\tEnter the name to search : ")
            searchAccountsByName(name)
        elif ch == '9':
            num = int(input("\tEnter The account No. : "))
            conn = sqlite3.connect('bank_management.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM accounts WHERE accNo = ?', (num,))
            row = cursor.fetchone()
            if row:
                account = Account(*row)
                account.apply_interest()
            else:
                print("No existing record with this number")
            conn.close()
        elif ch == '10':
            generateReport()
        elif ch == '11':
            print("\tThanks for using bank management system")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()