from app.extensions import db
from datetime import datetime, timezone


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(2000), nullable=False)
    amount = db.Column(db.Numeric(10,2), nullable=False)
    category = db.Column(db.String(2000), nullable=False)
    type = db.Column(db.String(2000), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

