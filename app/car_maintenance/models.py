from app import db
from datetime import date

class CarMaintenance(db.Model):
    __tablename__ = 'car_maintenance'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    mileage = db.Column(db.Integer, nullable=False)
    service = db.Column(db.String(200), nullable=False)
    amount_paid = db.Column(db.Float, nullable=False)
    service_provider = db.Column(db.String(200))
    notes = db.Column(db.Text)