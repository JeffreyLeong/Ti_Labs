from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from datetime import datetime
from decimal import Decimal
from app.extensions import db
from .models import Transaction, Category
from .forms import TransactionForm

expense_tracker = Blueprint(
    "expense_tracker",
    __name__,
    template_folder="templates",
)

# Dashboard page
@expense_tracker.route("/")
def dashboard():
    transactions = Transaction.query.order_by(Transaction.date.desc()).all()
    categories = Category.query.filter_by(active=True).order_by(Category.name).all()
    return render_template(
        "dashboard.html",
        transactions=transactions,
        categories=categories
    )


# Add transaction via AJAX
@expense_tracker.route("/add", methods=["POST"])
def add_record():
    data = request.json

    # Backend validation
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
        amount=float(data["amount"]),
        type=data["type"],
        category_id=category.id
    )

    db.session.add(tx)
    db.session.commit()

    return jsonify({
        "id": tx.id,
        "date": tx.date.strftime("%Y-%m-%d"),
        "description": tx.description,
        "amount": tx.amount,
        "type": tx.type,
        "category": category.name
    })


# Delete transaction via AJAX
@expense_tracker.route("/delete/<int:tx_id>", methods=["DELETE"])
def delete_record(tx_id):
    tx = Transaction.query.get(tx_id)
    if tx:
        db.session.delete(tx)
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"success": False}), 404

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
