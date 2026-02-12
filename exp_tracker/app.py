from flask import Flask, render_template, request, redirect, url_for, flash
import json
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "mysecretkey"

DATA_FILE = "data.json"

#createfile
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({"banks": {}}, f, indent=4)

#loaddata
def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

#savedata
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

#home
@app.route("/")
def welcome():
    return render_template("welcome.html")

#selectbank
@app.route("/select-bank", methods=["GET","POST"])
def select_bank():
    data = load_data()
    banks = data["banks"].keys()

    if request.method == "POST":
        bank = request.form.get("bank")
        if not bank:
            flash("Please select a bank","error")
            return redirect(url_for("select_bank"))
        return redirect(url_for("dashboard", bank=bank))

    return render_template("select_bank.html", banks=banks)

#balance
def calculate_balance(bank_data):
    balance = 0

    for sal in bank_data.get("SALARY", {}).values():
        if not sal.get("is_delete", False):
            balance += sal.get("AMOUNT",0)

    for exp in bank_data.get("EXPENSES", {}).values():
        if not exp.get("is_delete", False):
            balance -= exp.get("AMOUNT",0)

    return balance

#dashboard
@app.route("/dashboard/<bank>")
def dashboard(bank):
    data = load_data()
    bank_data = data["banks"].get(bank)

    if not bank_data:
        flash("Bank not found","error")
        return redirect(url_for("select_bank"))

    total_salary = 0
    total_expense = 0

    for sal in bank_data.get("SALARY", {}).values():
        if not sal.get("is_delete", False):
            total_salary += sal.get("AMOUNT",0)

    for exp in bank_data.get("EXPENSES", {}).values():
        if not exp.get("is_delete", False):
            total_expense += exp.get("AMOUNT",0)

    balance = total_salary - total_expense

    return render_template("dashboard.html",
        bank=bank,
        balance=balance,
        total_salary=total_salary,
        total_expense=total_expense
    )
#viewexpense
@app.route("/view-expenses/<bank>")
def view_expenses(bank):
    data = load_data()
    bank_data = data["banks"][bank]

    return render_template("view_expense.html",
        bank=bank,
        expenses=bank_data.get("EXPENSES", {}),
        balance=calculate_balance(bank_data)
    )

#addexpense
@app.route("/add-expense/<bank>", methods=["GET","POST"])
def add_expense(bank):
    data = load_data()
    bank_data = data["banks"][bank]

    if request.method == "POST":
        name = request.form["name"]
        amount = int(request.form["amount"])

        if amount > calculate_balance(bank_data):
            return render_template("form.html",
                title="Add Expense",
                button="Add Expense",
                item=None,
                back_url=url_for("view_expenses", bank=bank),
                error="Expense cannot exceed balance"
            )

        bank_data.setdefault("EXPENSES", {})
        exp_id = f"EXP{int(datetime.now().timestamp())}"

        bank_data["EXPENSES"][exp_id] = {
            "NAME":name,
            "AMOUNT":amount,
            "is_delete":False,
            "created_at":str(datetime.now()),
            "updated_at":str(datetime.now())
        }

        save_data(data)
        flash("Expense added","success")
        return redirect(url_for("view_expenses", bank=bank))

    return render_template("form.html",
        title="Add Expense",
        button="Add Expense",
        item=None,
        back_url=url_for("view_expenses", bank=bank)
    )

#updateexpense
@app.route("/update-expense/<bank>/<exp_id>", methods=["GET","POST"])
def update_expense(bank,exp_id):
    data = load_data()
    expense = data["banks"][bank].get("EXPENSES",{}).get(exp_id)

    if not expense or expense["is_delete"]:
        return redirect(url_for("view_expenses", bank=bank))

    if request.method == "POST":
        new_amount = int(request.form["amount"])
        diff = new_amount - expense["AMOUNT"]

        if diff > calculate_balance(data["banks"][bank]):
            return render_template("form.html",
                title="Update Expense",
                button="Update Expense",
                item=expense,
                back_url=url_for("view_expenses", bank=bank),
                error="Amount exceeds balance"
            )

        expense["NAME"] = request.form["name"]
        expense["AMOUNT"] = new_amount
        expense["updated_at"] = str(datetime.now())

        save_data(data)
        flash("Expense updated","success")
        return redirect(url_for("view_expenses", bank=bank))

    return render_template("form.html",
        title="Update Expense",
        button="Update Expense",
        item=expense,
        back_url=url_for("view_expenses", bank=bank)
    )
#deleteexpense
@app.route("/delete-expense/<bank>/<exp_id>", methods=["GET","POST"])
def delete_expense(bank,exp_id):
    data = load_data()
    expense = data["banks"][bank].get("EXPENSES",{}).get(exp_id)

    if not expense or expense["is_delete"]:
        return redirect(url_for("view_expenses", bank=bank))

    if request.method == "POST":
        expense["is_delete"] = True
        expense["updated_at"] = str(datetime.now())
        save_data(data)
        flash("Expense deleted","success")
        return redirect(url_for("view_expenses", bank=bank))

    return render_template("confirm_delete.html",
    type="Expense",
    item=expense,
    back_url=url_for("view_expenses", bank=bank)
)
#viewsalary
@app.route("/view-salary/<bank>")
def view_salary(bank):
    data = load_data()
    return render_template("view_salary.html",
        bank=bank,
        salary=data["banks"][bank].get("SALARY",{})
    )

#addsalary
@app.route("/add-salary/<bank>", methods=["GET","POST"])
def add_salary(bank):
    data = load_data()
    salary = data["banks"][bank].setdefault("SALARY",{})

    if request.method == "POST":
        sal_id = f"SAL{int(datetime.now().timestamp())}"

        salary[sal_id] = {
            "NAME":request.form["name"],
            "AMOUNT":int(request.form["amount"]),
            "is_delete":False,
            "created_at":str(datetime.now()),
            "updated_at":str(datetime.now())
        }

        save_data(data)
        flash("Salary added","success")
        return redirect(url_for("view_salary", bank=bank))

    return render_template("form.html",
        title="Add Salary",
        button="Add Salary",
        item=None,
        back_url=url_for("view_salary", bank=bank)
    )

#updatesalary
@app.route("/update-salary/<bank>/<sal_id>", methods=["GET","POST"])
def update_salary(bank,sal_id):
    data = load_data()
    sal = data["banks"][bank].get("SALARY",{}).get(sal_id)

    if not sal or sal["is_delete"]:
        return redirect(url_for("view_salary", bank=bank))

    if request.method == "POST":
        sal["NAME"] = request.form["name"]
        sal["AMOUNT"] = int(request.form["amount"])
        sal["updated_at"] = str(datetime.now())
        save_data(data)
        flash("Salary updated","success")
        return redirect(url_for("view_salary", bank=bank))

    return render_template("form.html",
        title="Update Salary",
        button="Update Salary",
        item=sal,
        back_url=url_for("view_salary", bank=bank)
    )

#deletesalary
@app.route("/delete-salary/<bank>/<sal_id>", methods=["GET","POST"])
def delete_salary(bank,sal_id):
    data = load_data()
    sal = data["banks"][bank].get("SALARY",{}).get(sal_id)

    if not sal or sal["is_delete"]:
        return redirect(url_for("view_salary", bank=bank))

    if request.method == "POST":
        sal["is_delete"] = True
        sal["updated_at"] = str(datetime.now())
        save_data(data)
        flash("Salary deleted","success")
        return redirect(url_for("view_salary", bank=bank))

    return render_template("confirm_delete.html",
    type="Salary",
    item=sal,
    back_url=url_for("view_salary", bank=bank)
)

#addbank
@app.route("/add-bank", methods=["GET","POST"])
def add_bank():
    data = load_data()

    if request.method == "POST":
        name = request.form["bank"].strip().upper()

        if name == "":
            flash("Bank name required","error")
            return redirect(url_for("add_bank"))

        if not name.isalpha():
            flash("Only letters allowed","error")
            return redirect(url_for("add_bank"))

        bank_key = name + "_BANK"

        if bank_key in data["banks"]:
            flash("Bank already exists","error")
            return redirect(url_for("add_bank"))

        data["banks"][bank_key] = {"EXPENSES":{}, "SALARY":{}}
        save_data(data)
        flash("Bank added","success")
        return redirect(url_for("select_bank"))

    return render_template("add_bank.html")

#deletebank
@app.route("/delete-bank/<bank>", methods=["GET","POST"])
def delete_bank(bank):
    data = load_data()

    if bank not in data["banks"]:
        flash("Bank not found","error")
        return redirect(url_for("select_bank"))

    if request.method == "POST":
        del data["banks"][bank]
        save_data(data)
        flash("Bank deleted","success")
        return redirect(url_for("select_bank"))

    return render_template(
    "confirm_delete.html",
    type="Bank",
    bank=bank,
    item=None,
    back_url=url_for("select_bank")
)

if __name__ == "__main__":
    app.run(debug=True)