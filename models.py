from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timedelta

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    foods = db.relationship('FoodItem', backref='owner', lazy=True)

class FoodItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow)
    storage = db.Column(db.String(50), default="room")
    quantity = db.Column(db.Integer, default=1)
    expiry_date = db.Column(db.DateTime, default=lambda: datetime.utcnow() + timedelta(days=7))
    status = db.Column(db.String(50), default="Fresh")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def check_status(self):
        today = datetime.utcnow()
        if today >= self.expiry_date:
            self.status = "Expired"
        elif today >= self.expiry_date - timedelta(days=2):
            self.status = "Expiring Soon"
        else:
            self.status = "Fresh"
        return self.status
