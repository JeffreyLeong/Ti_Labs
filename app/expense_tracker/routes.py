from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from datetime import datetime
from decimal import Decimal
from app.extensions import db
from .models import Transaction, Category
from .forms import TransactionForm
from sqlalchemy import func, extract

expense_tracker = Blueprint(
    "expense_tracker",
    __name__,
    template_folder="templates",
)

# Dashboard page
@expense_tracker.route("/")
def dashboard():
    now = datetime.now()
    year = now.year

    # Get selected month from query param, default to current month
    month = request.args.get("month", default=now.month, type=int)

    monthly_budget = 4000  # hardcoded

    # YTD totals
    ytd_income = db.session.query(func.sum(Transaction.amount))\
        .filter(Transaction.type == "income")\
        .filter(extract('year', Transaction.date) == year)\
        .scalar() or Decimal("0.00")

    ytd_expense = db.session.query(func.sum(Transaction.amount))\
        .filter(Transaction.type == "expense")\
        .filter(extract('year', Transaction.date) == year)\
        .scalar() or Decimal("0.00")

    ytd_savings = db.session.query(func.sum(Transaction.amount))\
        .filter(Transaction.type == "transfer")\
        .filter(extract('year', Transaction.date) == year)\
        .scalar() or Decimal("0.00")

    net_ytd = ytd_income - ytd_expense
    savings_rate = round((ytd_savings / ytd_income * 100), 1) if ytd_income else 0

    # Current month totals
    current_month_expense = db.session.query(func.sum(Transaction.amount))\
        .filter(Transaction.type == "expense")\
        .filter(extract('year', Transaction.date) == year)\
        .filter(extract('month', Transaction.date) == month)\
        .scalar() or Decimal("0.00")

    # Category breakdown for selected month
    category_totals = db.session.query(
        Category.name,
        func.sum(Transaction.amount)
    ).join(Transaction)\
     .filter(Transaction.type == "expense")\
     .filter(extract('year', Transaction.date) == year)\
     .filter(extract('month', Transaction.date) == month)\
     .group_by(Category.name)\
     .all()
    
    categories = Category.query.order_by(Category.name).all()

    budget_percentage = min(
        (current_month_expense / monthly_budget * 100),
        100
    ) if monthly_budget else 0

    return render_template(
        "dashboard.html",
        ytd_income=ytd_income,
        ytd_expense=ytd_expense,
        ytd_savings=ytd_savings,
        savings_rate=savings_rate,
        net_ytd=net_ytd,
        current_month_expense=current_month_expense,
        monthly_budget=monthly_budget,
        category_totals=category_totals,
        categories=categories,
        budget_percentage=budget_percentage,
        selected_month=month
    )
    
# Add transaction via AJAX
@expense_tracker.route("/add", methods=["POST"])
def add_record():
    data = request.json

    if not data.get("category_id"):
        return jsonify({"error": "Category is required"}), 400

    if not data.get("type"):
        return jsonify({"error": "Type is required"}), 400

    category = Category.query.get(data["category_id"])
    if not category:
        return jsonify({"error": "Invalid category"}), 400

    tx = Transaction(
        date=datetime.strptime(data["date"], "%Y-%m-%d"),
        description=data["description"],
        amount=Decimal(str(data["amount"])),
        type=data["type"],
        category_id=category.id
    )

    db.session.add(tx)
    db.session.commit()

    return jsonify({
        "id": tx.id,
        "date": tx.date.strftime("%Y-%m-%d"),
        "description": tx.description,
        "amount": float(tx.amount),
        "type": tx.type,
        "category": category.name
    })


# Delete transaction via AJAX
@expense_tracker.route("/delete/<int:tx_id>", methods=["POST"])
def delete_record(tx_id):
    tx = Transaction.query.get_or_404(tx_id)
    db.session.delete(tx)
    db.session.commit()
    return redirect(url_for("expense_tracker.view_all"))


@expense_tracker.route("/all")
def view_all():
    transactions = Transaction.query.order_by(Transaction.date.desc()).all()
    return render_template("view_all.html", transactions=transactions)


@expense_tracker.route("/add-form", methods=["GET", "POST"])
def add_transaction():
    form = TransactionForm()

    if form.validate_on_submit():
        tx = Transaction(
            date=form.date.data,
            description=form.description.data,
            amount=form.amount.data,
            type=form.type.data,
            category_id=form.category_id.data
        )
        db.session.add(tx)
        db.session.commit()
        return redirect(url_for("expense_tracker.dashboard"))

    return render_template("add_transaction.html", form=form)

@expense_tracker.route("/edit/<int:tx_id>", methods=["GET"])
def edit_record(tx_id):
    tx = Transaction.query.get_or_404(tx_id)
    categories = Category.query.all()
    return render_template("edit_record.html", tx=tx, categories=categories)

@expense_tracker.route("/edit/<int:tx_id>", methods=["POST"])
def update_record(tx_id):
    tx = Transaction.query.get_or_404(tx_id)

    tx.date = datetime.strptime(request.form["date"], "%Y-%m-%d")
    tx.amount = Decimal(request.form["amount"])
    tx.description = request.form["description"]
    tx.category_id = int(request.form["category"])
    tx.type = request.form["type"]

    db.session.commit()

    return redirect(url_for("expense_tracker.view_all"))