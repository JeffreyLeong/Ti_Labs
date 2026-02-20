from app.extensions import db
from datetime import datetime, timezone

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(2000), nullable=False)
    amount = db.Column(db.Numeric(10,2), nullable=False)
    
    # Old string field removed
    # category = db.Column(db.String(2000), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)

    type = db.Column(db.String(2000), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    active = db.Column(db.Boolean, default=True)

    transactions = db.relationship("Transaction", backref="category_obj", lazy=True)

    def __repr__(self):
        return f"<Category {self.name}>"
