from flask import Blueprint

car_maintenance = Blueprint(
    "car_maintenance",
    __name__,
    template_folder="templates",
)

@car_maintenance.route("/")
def index():
    return "Car Maintenance Home"