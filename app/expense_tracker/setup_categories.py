from app.extensions import db
from app.expense_tracker.models import Category

categories = sorted([
    "Car",
    "Dogs",
    "Eating Out",
    "Education & Loans",
    "Entertainment & Subscriptions",
    "Groceries",
    "Health",
    "Housing",
    "Income",
    "Miscellaneous",
    "Personal Care",
    "Savings & Investments",
    "Shopping",
    "Travel & Recreation"
])

for name in categories:
    if not Category.query.filter_by(name=name).first():
        db.session.add(Category(name=name))

db.session.commit()
print("Categories added!")
