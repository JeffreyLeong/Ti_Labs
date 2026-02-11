from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime
from decimal import Decimal
from app.extensions import db
from .models import Transaction

expense_tracker = Blueprint(
    "expense_tracker",
    __name__,
    template_folder="templates",
)

@expense_tracker.route("/")
def index():
    return "Expense Tracker Home"

@expense_tracker.route("/add", methods=["GET", "POST"])
def add_record():
    if request.method == "POST":
        date_str = request.form["date"]
        description = request.form["description"].strip()
        amount_str = request.form["amount"]
        category = request.form["category"]
        type_ = request.form["type"]

        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        amount = Decimal(amount_str)

        new_transaction = Transaction(
            date=date,
            description=description,
            amount=amount,
            category=category,
            type=type_
        )

        db.session.add(new_transaction)
        db.session.commit()

        return redirect(url_for("expense_tracker.index"))

    return render_template("add_transaction.html")