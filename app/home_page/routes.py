from flask import Blueprint

home_page = Blueprint(
    "home_page",
     __name__,
     )

@home_page.route("/")
def index():
    return "Welcome! Select from 'Tip Calculator', 'Expense Tracker', 'Car Maintenance'."