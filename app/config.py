import os
from dotenv import load_dotenv

load_dotenv()  # loads .env variables

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f"postgresql://admin:{os.getenv('DB_PASSWORD')}@localhost/ti_labs_new"