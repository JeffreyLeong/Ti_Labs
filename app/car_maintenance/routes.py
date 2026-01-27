from flask import Blueprint

car_maintenance = Blueprint(
    "car_maintenance",
    __name__,
    url_prefix="/car_maintenance"
)

@car_maintenance.route("/")
def index():
    return "Car Maintenance Home"