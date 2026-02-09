import tabulate as t
import time
# ANSI Color Codes
RESET = "\033[0m"
BLACK = "\033[30m\033[1m"
RED = "\033[31m\033[1m"
GREEN = "\033[32m\033[1m"
YELLOW = "\033[33m\033[1m"
BLUE = "\033[34m\033[1m"
MAGENTA = "\033[35m\033[1m"
CYAN = "\033[36m\033[1m"
WHITE = "\033[37m\033[1m"
names = []
paid = {}
shares = {}
debtors = []
creditors = []
tableData = []
currency_symbols = {"usd":"$", "eur":"€", "jpy":"¥", "gbp":"£", "inr":"₹"}
# FUNCTION TO GET REQUIRED CURRENCY
def getCurrency():
        while True:
            try:
                currency = input(f"{BLUE}Enter the currency you will be using (eg: USD)):{RESET} ").lower()
                symbol = currency_symbols.get(currency)
                if symbol: 
                    print(f"{YELLOW}OK!{RESET}")
                    print(f"{YELLOW}This recorder will record expenses in {currency.upper()}{RESET}")
                    break
                else:
                    print(f"{RED}Currency not found! Try Again!{RESET}")
                    continue
            except ValueError:
                print(f"{RED}Value error raised! Try again!{RESET}")
                continue
        return symbol
# FUNCTION TO GET REQUIRED NUMBERS(EXPENSES,PEOPLE,NAMES)
def getNumber():
        while True:
            try:
                number_people = int(input(f"{BLUE}Enter the number of people: {RESET}"))
                for i in range(1,number_people+1):
                    name_person = (input(f"{BLUE}Name of person {i}: {RESET}")).capitalize()
                    names.append(name_person)
                    paid[name_person]=0
                    shares[name_person]=0
                number_expense = int(input(f"{BLUE}Enter the number of expenses: {RESET}"))
                return number_expense
            except ValueError:
                print(f"{RED}Value error raised! Try again!{RESET}")
                continue
# FUNCTION TO RECORD DETAILS OF EVERY EXPENSE            
def expenseRecorder(number_expense):
        while True:
            try:   
                for x in range(1,number_expense+1):
                    print("="*45)
                    print(f"{GREEN}Expense {x}{RESET}")
                    print("="*45)
                    while True:
                        whoPaid = input(f"{BLUE}Name of the person who paid for this expense: {RESET}").capitalize()
                        if whoPaid in names:
                            break
                        time.sleep(1)
                        print(f"{GREEN}Not in name list! Please enter again{RESET}")
                    amountPaid = float(input(f"{BLUE}Enter amount paid: {RESET}"))
                    paid[whoPaid] += amountPaid
                    expensePeople = int(input(f"{BLUE}Number of people who shared this expense: {RESET}"))
                    share_perHead = (amountPaid / expensePeople)
                    for a in range(1, expensePeople+1):
                        while True:
                            expenseName = input(f"{BLUE}Enter name of person {a}: {RESET}").capitalize()
                            if expenseName in names:
                                break
                            time.sleep(1)
                            print(f"{RED}Not in name list! Please enter again{RESET}")
                        shares[expenseName] += share_perHead
            except ValueError:
                print(f"{RED}Value error raised! Try again!{RESET}")
                continue 
# FUNCTION TO PRINT STATEMENTS BASED ON EXPENSES
def printExpenseRecord(number_expense):
        if number_expense > 1:
            print("="*45)
            print(f"{CYAN}Expenses recorded succesfully!{RESET}")
            print("="*45)
        elif number_expense == 1:
            print("="*45)
            print(f"{CYAN}Expense recorded succesfully!{RESET}")
            print("="*45)
# FUNCTION TO RECORD DATA TO CREATE A TABLE
def tableDataRecorder(symbol):
        for name in names:
            paid_amount = paid[name]
            share_amount = shares[name]
            balance = paid_amount - share_amount
            tableData.append([name, f"{symbol}{paid_amount:.2f}", f"{symbol}{share_amount:.2f}", f"{symbol}{balance:.2f}"])
            if balance > 0:
                creditors.append((name,balance))
            elif balance < 0:
                debtors.append((name,abs(balance)))
# FUNCTION TO CREATE A TABLE WITH ALL DATA
def tableCreator():
        headers = ["Name", "Amount Paid", "Total Share", "Balance Per Head"]
        print("="*45)
        print(f"{RED}OVERVIEW OF EXPENSES{RESET}")
        print("="*45)
        time.sleep(1)
        print(t.tabulate(tableData, headers=headers, tablefmt="grid"))
# FUNCTION CONTAINING ALGORITHM TO CALCULATE DEBT AND CREDIT
def debtLogic(symbol):
        while debtors and creditors:
            debtor_name, debtor_balance = debtors[0]
            creditor_name, creditor_balance = creditors[0]
            payment = min(debtor_balance,creditor_balance)
            print(f"{debtor_name} owes {creditor_name} {symbol}{payment}")
            debtor_balance -= payment
            creditor_balance -= payment
            if debtor_balance == 0:
                debtors.pop(0)
            else:
                debtors[0] = (debtor_name, debtor_balance)
            if creditor_balance == 0:
                creditors.pop(0)
            else:
                creditors[0] = (creditor_name, creditor_balance)
# MAIN BODY OF THE CODE
def main():
    symbol = getCurrency()
    number_expense = getNumber()
    expenseRecorder(number_expense)
    time.sleep(1)
    printExpenseRecord(number_expense)
    tableDataRecorder(symbol)
    tableCreator()
    time.sleep(1.5)
    debtLogic(symbol)
    
if __name__ == "__main__":
     main()
