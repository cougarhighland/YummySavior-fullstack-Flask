"""Models for objects to be stored in database."""
from . import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    """User object model class."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    businessname = db.Column(db.String(45), unique=True, nullable=False)
    location = db.Column(db.String(30), nullable=False)
    user_type = db.Column(db.String(30), nullable=False)
    foods = db.relationship('Food', backref=db.backref('user'), lazy=True)


class Food(db.Model):
    """Food object model class."""

    id = db.Column(db.Integer, primary_key=True)
    food_name = db.Column(db.String(25))
    description = db.Column(db.String(25))
    quantity = db.Column(db.Integer())
    users_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def repr(self):
        """Format the food name output."""
        return "<food_name: {}>".format(self.food_name)


class Order(db.Model):
    """Order model class."""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.DateTime, nullable=False)
    details = db.relationship('OrderDetails', backref='order', lazy=False)


class OrderDetails(db.Model):
    """Order details model class."""

    food_id = db.Column(db.Integer, db.ForeignKey('food.id'), primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
