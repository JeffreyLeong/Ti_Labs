from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from datetime import datetime
from decimal import Decimal
from app.extensions import db
from .models import Transaction

expense_tracker = Blueprint(
    "expense_tracker",
    __name__,
    template_folder="templates",
)

# Dashboard page
@expense_tracker.route("/")
def dashboard():
    transactions = Transaction.query.order_by(Transaction.date.desc()).limit(10)
    return render_template("dashboard.html", transactions=transactions)

# Add transaction via AJAX
@expense_tracker.route("/add", methods=["POST"])
def add_record():
    data = request.json
    date = datetime.strptime(data["date"], "%Y-%m-%d").date()
    description = data["description"].strip()
    amount = Decimal(data["amount"])
    category = data.get("category", "")
    type_ = data.get("type", "")

    new_tx = Transaction(
        date=date,
        description=description,
        amount=amount,
        category=category,
        type=type_
    )

    db.session.add(new_tx)
    db.session.commit()

    return jsonify({
        "id": new_tx.id,
        "date": str(new_tx.date),
        "description": new_tx.description,
        "amount": str(new_tx.amount),
        "category": new_tx.category,
        "type": new_tx.type
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
