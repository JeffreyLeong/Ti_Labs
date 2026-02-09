from flask import Blueprint

expense_tracker = Blueprint(
    "expense_tracker",
    __name__,
    template_folder="templates",
)

@expense_tracker.route("/")
def index():
    return "Expense Tracker Home"