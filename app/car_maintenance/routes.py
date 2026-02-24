from flask import Blueprint, render_template, request, redirect, url_for
from .db import get_db_connection

car_maintenance = Blueprint(
    "car_maintenance",
    __name__,
    template_folder="templates",
)

# --- VIEW ALL RECORDS ---
@car_maintenance.route("/")
def index():
    conn = get_db_connection()
    records = conn.execute("SELECT * FROM car_maintenance ORDER BY date DESC").fetchall()
    conn.close()
    return render_template("index.html", records=records)

# --- ADD RECORD ---
@car_maintenance.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        date = request.form["date"]
        mileage = request.form["mileage"]
        service = request.form["service"]
        amount_paid = request.form["amount_paid"]
        service_provider = request.form.get("service_provider")
        notes = request.form.get("notes")

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO car_maintenance (date, mileage, service, amount_paid, service_provider, notes) VALUES (?, ?, ?, ?, ?, ?)",
            (date, mileage, service, amount_paid, service_provider, notes)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("car_maintenance.index"))

    return render_template("add.html")

# --- EDIT RECORD ---
@car_maintenance.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = get_db_connection()
    record = conn.execute("SELECT * FROM car_maintenance WHERE id = ?", (id,)).fetchone()

    if not record:
        conn.close()
        return redirect(url_for("car_maintenance.index"))

    if request.method == "POST":
        date = request.form["date"]
        mileage = request.form["mileage"]
        service = request.form["service"]
        amount_paid = request.form["amount_paid"]
        service_provider = request.form.get("service_provider")
        notes = request.form.get("notes")

        conn.execute(
            "UPDATE car_maintenance SET date=?, mileage=?, service=?, amount_paid=?, service_provider=?, notes=? WHERE id=?",
            (date, mileage, service, amount_paid, service_provider, notes, id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("car_maintenance.index"))

    conn.close()
    return render_template("edit.html", record=record)

# --- DELETE RECORD ---
@car_maintenance.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM car_maintenance WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("car_maintenance.index"))