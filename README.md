# Ti_Labs

Ti_Labs is a personal web application built with Flask and PostgreSQL for tracking car maintenance and expenses. It includes a simple login system to restrict access.

## Features

- Car maintenance tracker
- Expense tracker
- User authentication with Flask-Login
- PostgreSQL database backend

## Requirements

- Python 3.10+
- PostgreSQL
- pip packages: Flask, Flask-Login, Flask-Migrate, Flask-SQLAlchemy, psycopg2-binary, python-dotenv, Werkzeug

## Setup

1. **Clone the repository**

```bash
git clone <your-repo-url>
cd Ti_Labs

Create and activate a virtual environment

python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

Install dependencies

pip install -r requirements.txt

Configure environment variables

Create a .env file in the root directory:

SECRET_KEY=your-secret-key
DB_PASSWORD=your-postgres-password

Update app/config.py if needed for your PostgreSQL connection.

Set up the database

Make sure your PostgreSQL user and database exist. For example:

-- In psql or pgAdmin
CREATE DATABASE ti_labs_db;
CREATE USER ti_labs_user WITH PASSWORD 'your-postgres-password';
GRANT ALL PRIVILEGES ON DATABASE ti_labs_db TO ti_labs_user;

Initialize database tables

flask db upgrade

(Optional) Create an initial user

If this is your first time running the app locally:

from app import create_app, db
from app.models import User

app = create_app()
app.app_context().push()

user = User(username="your-username")
user.set_password("your-password")
db.session.add(user)
db.session.commit()

Note: This only affects your local database. Other users cloning the repo will not see your data.

Running the app
flask run

Navigate to http://127.0.0.1:5000 and log in with the user you created.

Notes

Only authenticated users can access the main functionality.

All sensitive information like passwords should be set via .env and never committed to GitHub.
