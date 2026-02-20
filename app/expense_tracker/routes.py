from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from datetime import datetime
from decimal import Decimal
from app.extensions import db
from .models import Transaction, Category

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
