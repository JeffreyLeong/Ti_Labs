from flask import Blueprint, render_template

tip_calculator = Blueprint(
    "tip_calculator",
    __name__,
    template_folder="templates",
)

@tip_calculator.route("/")
def index():
    return render_template("tip_calculator.html")