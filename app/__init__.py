from flask import Flask
from app.extensions import db, migrate
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.home_page.routes import home_page
    from app.car_maintenance.routes import car_maintenance 
    from app.expense_tracker.routes import expense_tracker
    from app.tip_calculator.routes import tip_calculator

    app.register_blueprint(home_page, url_prefix="/")
    app.register_blueprint(car_maintenance, url_prefix="/car_maintenance")
    app.register_blueprint(expense_tracker, url_prefix="/expense_tracker")
    app.register_blueprint(tip_calculator, url_prefix="/tip_calculator")

    

    return app