import tabulate as t
import time
import pandas as pd
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
# HELPER: Get integer
def get_int(prompt, error_message = "Please enter a valid number"):
     while True:
          try:
               return int(input(prompt))
          except ValueError:
               print(f"{RED}{error_message}{RESET}")
# HELPER: Get float
def get_float(prompt,error_message = "Please enter a valid number"):
     while True:
          try:
               value = float(input(prompt))
               if value < 0:
                    print(f"{RED}Amount cannot be negative! Try again!")
                    continue
               return value
          except ValueError:
               print(f"{RED}{error_message}{RESET}")
# HELPER: Get name
def get_valid_name(prompt,valid_names):
     while True:
          name=input(prompt).capitalize()
          if name in valid_names:
               return name
          print(f"{RED}Name not found. Available names are: {', '.join(valid_names)}{RESET}")
                                            
# MAIN MENU
def main_menu():
     print("\n" + "="*45)
     print(f"{CYAN}WELCOME TO THE EXPENSE SPLITTER{RESET}")
     print("="*45)
     print("1.Start new expense session")
     print("2.How it works")
     print("3.Exit")

     while True:
          choice = input("Choose an option(1-3):")
          if choice in ["1","2","3"]:
               return choice
          print(f"{RED}Invalid choice! Try again!")

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
        number_people = get_int(f"{BLUE}Enter number of people: {RESET}")
        for i in range(1,number_people+1):
            while True:
                name_person = (input(f"{BLUE}Name of person {i}: {RESET}")).capitalize()
                if not name_person.strip():
                    print(f"{RED}Name cannot be empty!{RESET}")
                    continue
                if name_person in names:
                    print(f"{RED}This name has already been entered. Please enter a unique name")
                    continue
                names.append(name_person) 
                paid[name_person]=0
                shares[name_person]=0
                break
        number_expense = get_int(f"{BLUE}Enter the number of expenses: {RESET}")
        return number_expense
            
# FUNCTION TO RECORD DETAILS OF EVERY EXPENSE            
def expenseRecorder(number_expense):
    for x in range(1,number_expense+1):
        print("="*45)
        print(f"{GREEN}Expense {x}{RESET}")
        print("="*45)
        whoPaid = get_valid_name(f"{BLUE}Name of the person who paid for this expense: {RESET}",names).capitalize()
        amountPaid = get_float(f"{BLUE}Enter amount paid: {RESET}")
        paid[whoPaid] += amountPaid
        while True:
            expensePeople = get_int(f"{BLUE}Number of people who shared this expense: {RESET}")
            if expensePeople > len(names):
                print(f"{RED}There are only {len(names)} people in the group! Try again{RESET}")
                continue
            if expensePeople <= 0:
                print(f"{RED}At least one person must share the expense. Try again!{RESET}")
                continue
            break
        share_perHead = (amountPaid / expensePeople)
        used_names = set()
        for a in range(1, expensePeople+1):
                while True:
                    expenseName = get_valid_name(f"{BLUE}Enter name of person {a}: {RESET}",names).capitalize()
                    if expenseName in used_names:
                        print(f"{RED}{expenseName} is already in the list! Try again{RESET}")
                        continue
                    used_names.add(expenseName)
                    shares[expenseName] += share_perHead
                    break
        
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
        print(t.tabulate(tableData, headers=headers, tablefmt="fancy_grid",stralign="center",numalign="center"))
# FUNCTION CONTAINING ALGORITHM TO CALCULATE DEBT AND CREDIT
def debtLogic(symbol):
        print("="*45)
        print(f"{RED}SUMMARY OF BALANCES{RESET}")
        print("="*45)

        for name in names:
            balance = paid[name] - shares[name]
            
            if balance > 0:
                print(f"{GREEN}{name} should receive {symbol}{balance:.2f}{RESET}")
            elif balance < 0:
                print(f"{RED}{name} owes {symbol}{abs(balance):.2f}{RESET}")
            else:
                print(f"{YELLOW}{name} is settled up{RESET}")
# SETTLEMENT BREAKDOWN
def settlement_breakdown(symbol):
    print("="*45)
    print(f"{BLUE}PAYMENT SETTLEMENT BREAKDOWN{RESET}")
    print("="*45)

    creditors=[]
    debtors = []

    for name in names:
        balance = paid[name]-shares[name]
        if balance > 0:
            creditors.append([name,balance])
        elif balance < 0:
            debtors.append([name,-balance])
        
    i = 0
    j = 0

    while i < len(debtors) and j < len(creditors):
        debtor,debt_amount = debtors[i]
        creditor, credit_amount = creditors[j]
        payment = min(debt_amount,credit_amount)
        print(f"{YELLOW}{debtor}{RESET} pays {GREEN}{creditor}{RESET} {symbol}{payment:.2f}")
        debtors[i][1] -= payment
        creditors[j][1] -= payment
        if debtors[i][1] == 0:
            i += 1
        if creditors[j][1] == 0:
             j += 1


        
     
# EXPORT TO EXCEL(.xlsx) OR CSV(.csv)
def export_data():
    df = pd.DataFrame(tableData, columns=["Name", "Amount Paid", "Total Share", "Balance Per Head"])
    print("\nWould you like to export the data?")
    print("1.Export as an Excel file(.xlsx)")
    print("2.Export as a CSV(.csv)")
    print("3.No, skip export")
    choice = input("Choose an option(1-3): ")
    if choice == "1":
         df.to_excel("expense_report.xlsx", index=False)
         print(f"{GREEN}Exported as expense_report.xlsx{RESET}")
    elif choice == "2":
         df.to_csv("expense_report.csv", index=False)
         print(f"{GREEN}Exported as expense_report.csv{RESET}")
    elif choice == "3":
         print(f"{YELLOW}Skipping export...{RESET}")

# DATA RESET
def data_reset():
    names.clear()
    paid.clear()
    shares.clear()
    debtors.clear()
    creditors.clear()
    tableData.clear()    
     
# MAIN BODY OF THE CODE
def main():
    while True:
        choice = main_menu()
        if choice == "1":
            data_reset()
            symbol = getCurrency()
            number_expense = getNumber()
            expenseRecorder(number_expense)
            time.sleep(1)
            printExpenseRecord(number_expense)
            tableDataRecorder(symbol)
            tableCreator()
            time.sleep(1.5)
            debtLogic(symbol)
            settlement_breakdown(symbol)
            export_data()
        elif choice == "2":
             print("This tool is useful in recording expenses and it provides debt and credit logic with an advanced algorithm. Enjoy!")
        elif choice =="3":
             print(f"{GREEN}Goodbye!{RESET}")
             break 
            
    
if __name__ == "__main__":
     main()