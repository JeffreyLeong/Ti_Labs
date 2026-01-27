from flask import Blueprint

expense_tracker = Blueprint(
    "expense_tracker",
    __name__,
    url_prefix="/expense_tracker"
)

@expense_tracker.route("/")
def index():
    return "Expense Tracker Home"