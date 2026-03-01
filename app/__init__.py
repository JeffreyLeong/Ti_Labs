from flask import Flask, session
from flask_login import current_user
from app.extensions import db, migrate
from app.auth import login_manager
from app.expense_tracker.cli import init_categories
from app.config import CurrentConfig

def create_app():
    app = Flask(__name__)
    app.config.from_object(CurrentConfig)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Import and register blueprints
    from app.auth.routes import auth_bp
    from app.home_page.routes import home_page
    from app.car_maintenance.routes import car_maintenance
    from app.expense_tracker.routes import expense_tracker
    from app.tip_calculator.routes import tip_calculator

    app.register_blueprint(auth_bp)
    app.register_blueprint(home_page, url_prefix="/")
    app.register_blueprint(car_maintenance, url_prefix="/car_maintenance")
    app.register_blueprint(expense_tracker, url_prefix="/expense_tracker")
    app.register_blueprint(tip_calculator, url_prefix="/tip_calculator")

    app.cli.add_command(init_categories)

    # Global login gate
    @app.before_request
    def require_login():
        from flask import redirect, request, url_for
        allowed_routes = ["auth.login", "static"]
        if request.endpoint not in allowed_routes and not current_user.is_authenticated:
            return redirect(url_for("auth.login"))

    # Rolling session timeout
    @app.before_request
    def refresh_session():
        if current_user.is_authenticated:
            session.permanent = True

    return app