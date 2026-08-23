import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MONTHLY_EXPENSE_BUDGET = 9000
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=5)

class DevConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f"postgresql://ti_labs_user:{os.getenv('DEV_DB_PASSWORD')}@localhost/ti_labs_db"

class ProdConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f"postgresql://admin:{os.getenv('PROD_DB_PASSWORD')}@44.246.45.4/ti_labs_new"

# Select config based on environment
if os.getenv("FLASK_ENV") == "production":
    CurrentConfig = ProdConfig
else:
    CurrentConfig = DevConfig