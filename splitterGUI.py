import customtkinter as ctk
import pandas as pd
import time
from tkinter import messagebox


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
table_data = []
currency_symbols = {"usd":"$", "eur":"€", "jpy":"¥", "gbp":"£", "inr":"₹"}

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")
app = ctk.CTk()
app.title("Expense Splitter")
app.after(1, app.wm_state, 'zoomed')

step = 0
symbol = ""
number_people = 0
number_expense = 0

current_name_index = 0

current_expense_index = 0
current_expense_payer = ""
current_expense_amount = 0
current_expense_people_count = 0
current_expense_share = 0
current_expense_person_index = 0
current_expense_used_names = set()

title_label = ctk.CTkLabel(app, text="Expense Splitter", font=("Arial",24,"bold"))
title_label.pack(pady=10)

prompt_label = ctk.CTkLabel(app, text="Enter the currency you will be using:",font=("Arial",16))
prompt_label.pack(pady=10)

entry = ctk.CTkEntry(app, width=300, placeholder_text="Type here...")
entry.pack(pady=5)

next_button = ctk.CTkButton(app,text="Next",corner_radius=20)
next_button.pack(pady=5)

output_box = ctk.CTkTextbox(app, width=650, height=300)
output_box.pack(pady=10)

def append_output(text):
    output_box.insert("end", text + "\n")
    output_box.see("end")

def data_reset():
    names.clear()
    paid.clear()
    shares.clear()
    debtors.clear()
    creditors.clear()
    table_data.clear()

def table_data_recorder():
    global table_data, creditors, debtors
    creditors = []
    debtors = []
    table_data = []

    for name in names:
        paid_amount = paid[name]
        share_amount = shares[name]
        balance = paid_amount - share_amount
        table_data.append([name, f"{symbol}{paid_amount:.2f}",f"{symbol}{share_amount:.2f}",f"{symbol}{balance:.2f}"])
        if balance > 0:
            creditors.append((name,balance))
        elif balance < 0:
            debtors.append((name,abs(balance))) 
def debt_logic():
    append_output("="*45)
    append_output("SUMMARY OF BALANCES")
    append_output("="*45)

    for name in names:
        balance = paid[name] - shares[name]
        if balance > 0:
            append_output(f"{name} should receive {symbol}{balance:.2f}")
        elif balance < 0:
            append_output(f"{name} owes {symbol}{abs(balance):.2f}")
        else:
            append_output(f"{name} is all settled up")
def settlement_breakdown():
    append_output("="*45)
    append_output("SETTLEMENT BREAKDOWN")
    append_output("="*45)

    local_creditors = []
    local_debtors = []

    for name in names:
        balance = paid[name] - shares[name]
        if balance > 0:
            local_creditors.append([name,balance])
        elif balance < 0:
            local_debtors.append([name,abs(balance)])

    i = 0
    j = 0

    while i < len(local_debtors) and j < len(local_creditors):
        debtor, debt_amount = local_debtors[i]
        creditor, credit_amount = local_creditors[j]
        payment = min(debt_amount, credit_amount)
        append_output(f"{debtor} pays {creditor} {symbol}{payment:.2f}")
        local_debtors[i][1] -= payment
        local_creditors[j][1] -= payment
        if local_debtors[i][1] == 0:
            i += 1
        if local_creditors[j][1] == 0:
            j += 1
def export_data():
    if not table_data:
        messagebox.showinfo("Export","No data to export")
        return
    df = pd.DataFrame(table_data,columns=["Name", "Amount Paid", "Total Share", "Balance Per Head"])

    export_window = ctk.CTkToplevel(app)
    export_window.title("Export Data")
    export_window.geometry("300x200")
    export_window.lift()
    export_window.focus_force()
    export_window.grab_set()

    label = ctk.CTkLabel(export_window,text="Export data as: ")
    label.pack(pady=10)

    def export_excel():
        df.to_excel("expense_report.xlsx", index=False)
        messagebox.showinfo("Export", "Exported as expense_report.xlsx")
    def export_csv():
        df.to_csv("expense_report.csv",index=False)
        messagebox.showinfo("Export","Exported as expense_report.csv")
    
    btn_excel = ctk.CTkButton(export_window,text="Excel",command=export_excel)
    btn_excel.pack(pady=5)

    btn_csv = ctk.CTkButton(export_window,text="CSV",command=export_csv)
    btn_csv.pack(pady=10)

    btn_close = ctk.CTkButton(export_window,text="Close",fg_color="#b71c1c",command=export_window.destroy)
    btn_close.pack(pady=10)

def handle_currency(user_input):
    global symbol, step
    cur = user_input.lower()
    sym = currency_symbols.get(cur)
    if not sym:
        messagebox.showerror("Error","Currency not found! Try Again")
        return
    symbol = sym
    append_output(f"Using currency: {cur.upper()} ({symbol})")
    prompt_label.configure(text="Enter number of people: ")
    step = 1
def handle_number_people(user_input):
    global number_people,step,current_name_index
    try:
        n = int(user_input)
        if n <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error","Please enter a valid positive number of people")
    number_people = n
    current_name_index = 0
    prompt_label.configure(text=f"Enter name of person {current_name_index + 1}:")
    step = 2
def handle_names(user_input):
    global current_name_index,step
    name_person = user_input.capitalize()
    if not name_person.strip():
        messagebox.showerror("Error","Name field cannot be left empty")
        return
    if name_person in names:
        messagebox.showerror("Error","Name cannot be repeated. It must be unique")
        return
    names.append(name_person)
    paid[name_person] = 0
    shares[name_person] = 0
    current_name_index += 1
    if current_name_index < number_people:
        prompt_label.configure(text=f"Enter name of person {current_name_index + 1}: ")
    else:
        prompt_label.configure(text="Enter number of expenses: ")
        step = 3
def handle_number_expenses(user_input):
    global number_expense, step, current_expense_index
    try:
        ne = int(user_input)
        if ne <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error","Enter a valid positive number")
        return
    number_expense = ne
    current_expense_index = 0
    append_output(f"Recording {number_expense} expense(s)...")
    prompt_label.configure(text=f"Expense 1: Enter name of person who paid:")
    step = 4

def handle_expenses(user_input):
    global current_expense_index,current_expense_payer,current_expense_amount
    global current_expense_people_count,current_expense_share
    global current_expense_person_index,current_expense_used_names,step

    text = prompt_label.cget("text")
    if "who paid" in text:
        name = user_input.capitalize()
        if name not in names:
            messagebox.showerror("Error",f"Name not found. Available names are: {', '.join(names)}")
            return
        current_expense_payer = name
        prompt_label.configure(text=f"Expense {current_expense_index + 1}: Enter amount paid: ")
        return
    if "amount paid" in text:
        try:
            amt = float(user_input)
            if amt < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error","Enter a valid positive amount")
            return
        current_expense_amount = amt
        paid[current_expense_payer] += amt
        prompt_label.configure(text=f"Expense {current_expense_index + 1}: Number of people who shared this expense: ")
        return
    if "Number of people who shared" in text:
        try:
            cnt = int(user_input)
            if cnt <= 0:
                raise ValueError
            if cnt > len(names):
                raise ValueError
        except ValueError:
            messagebox.showerror("Error",f"Please enter a positive number(atleast 1). Make sure the number is not greater than {len(names)}")
            return
        current_expense_people_count = cnt
        current_expense_share = current_expense_amount/current_expense_people_count
        current_expense_person_index = 0
        current_expense_used_names = set()
        prompt_label.configure(text=f"Expense {current_expense_index + 1}: Enter the name of person {current_expense_person_index + 1} who shared: ")
        return
    if "who shared" in text:
        name = user_input.capitalize()
        if name not in names:
            messagebox.showerror("Error","Name not found")
            return
        if name in current_expense_used_names:
            messagebox.showerror("Error",f"{name} has already been added")
            return
        current_expense_used_names.add(name)
        shares[name] += current_expense_share
        current_expense_person_index += 1

        if current_expense_person_index < current_expense_people_count:
            prompt_label.configure(text=f"Expense {current_expense_index + 1}: Enter name of person {current_expense_person_index + 1} who shared: ")
        else:
            current_expense_index += 1
            if current_expense_index < number_expense:
                prompt_label.configure(text=f"Expense {current_expense_index + 1}: Enter name of the person who paid: ")
            else:
                append_output("All expenses recorded successfully!")
                table_data_recorder()
                append_output("="*45)
                append_output("OVERVIEW OF EXPENSES")
                append_output("="*45)
                for row in table_data:
                    append_output(f"{row[0]:<10} {row[1]:<10} {row[2]:<10}")
                time.sleep(0.5)
                debt_logic()
                settlement_breakdown()
                step = 5
                prompt_label.configure(text="All done. You can either export or reset.")
            return

def next_control():
    global step
    user_input = entry.get().strip()
    entry.delete(0, "end")

    if step == 0:
        handle_currency(user_input)
    elif step == 1:
        handle_number_people(user_input)
    elif step == 2:
        handle_names(user_input)
    elif step == 3:
        handle_number_expenses(user_input)
    elif step == 4:
        handle_expenses(user_input)
    elif step == 5:
        messagebox.showinfo("Info","Process complete. Export data or reset.")

next_button.configure(command=next_control)

button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=5)

export_button = ctk.CTkButton(button_frame, text="Export Data", command=export_data, corner_radius=20)
export_button.grid(row=0, column=0, padx=5)


def reset_session():
    global step, symbol, number_people, number_expense
    global current_name_index, current_expense_index
    global current_expense_payer, current_expense_amount
    global current_expense_people_count, current_expense_share
    global current_expense_person_index, current_expense_used_names

    data_reset()
    step = 0
    symbol = ""
    number_people = 0
    number_expense = 0
    current_name_index = 0
    current_expense_index = 0
    current_expense_payer = ""
    current_expense_amount = 0.0
    current_expense_people_count = 0
    current_expense_share = 0.0
    current_expense_person_index = 0
    current_expense_used_names = set()

    output_box.delete("1.0", "end")
    prompt_label.configure(text="Enter the currency you will be using:")

reset_button = ctk.CTkButton(button_frame, text="Reset Session", command=reset_session, corner_radius=20, fg_color="#b71c1c")
reset_button.grid(row=0, column=1, padx=5)


app.bind("<Return>", lambda event: next_control())
app.bind("<Escape>", lambda event: app.destroy())
app.mainloop()
