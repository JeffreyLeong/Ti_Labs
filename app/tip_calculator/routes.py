from flask import Blueprint

tip_calculator = Blueprint(
    "tip_calculator",
    __name__,
    url_prefix="/tip_calculator"
)

@tip_calculator.route("/")
def index():
    return "Tip Calculator Home"