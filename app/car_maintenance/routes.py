from flask import Blueprint, render_template, request, redirect, url_for
from .models import CarMaintenance
from app import db

car_maintenance = Blueprint(
    "car_maintenance",
    __name__,
    template_folder="templates",
)

# --- VIEW ALL RECORDS ---
@car_maintenance.route("/")
def index():
    records = CarMaintenance.query.order_by(CarMaintenance.date.desc()).all()
    return render_template("index.html", records=records)

# --- ADD RECORD ---
@car_maintenance.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        record = CarMaintenance(
            date=request.form["date"],
            mileage=request.form["mileage"],
            service=request.form["service"],
            amount_paid=request.form["amount_paid"],
            service_provider=request.form.get("service_provider"),
            notes=request.form.get("notes")
        )
        db.session.add(record)
        db.session.commit()
        return redirect(url_for("car_maintenance.index"))

    return render_template("add.html")

# --- EDIT RECORD ---
@car_maintenance.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    record = CarMaintenance.query.get_or_404(id)

    if request.method == "POST":
        record.date = request.form["date"]
        record.mileage = request.form["mileage"]
        record.service = request.form["service"]
        record.amount_paid = request.form["amount_paid"]
        record.service_provider = request.form.get("service_provider")
        record.notes = request.form.get("notes")
        db.session.commit()
        return redirect(url_for("car_maintenance.index"))

    return render_template("edit.html", record=record)

# --- DELETE RECORD ---
@car_maintenance.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    record = CarMaintenance.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    return redirect(url_for("car_maintenance.index"))