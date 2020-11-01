from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask import redirect, url_for, session


db = SQLAlchemy()


class LoginMixin:

    def is_accessible(self):
        return bool(session.get('user_id'))

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login'))


class OrdersMeals(db.Model):
    __tablename__ = 'orders_meals'
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), primary_key=True)
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'), primary_key=True)
    meal_amount = db.Column(db.Integer, nullable=False)
    meal_sum = db.Column(db.Integer, nullable=False)
    orders = db.relationship('Order', back_populates='meals')
    meals = db.relationship('Meal', back_populates='orders')


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(32), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    user_orders = db.relationship('Order', back_populates='user')

    def password_set(self, password):
        # Устанавливаем пароль через этот метод
        self.password_hash = generate_password_hash(password)

    def password_valid(self, password):
        # Проверяем пароль через этот метод
        # Функция check_password_hash превращает password в хеш и сравнивает с хранимым
        return check_password_hash(self.password_hash, password)


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    sum = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String, nullable=False)
    mail = db.Column(db.String, db.ForeignKey('users.mail'))
    phone = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    user = db.relationship('User', back_populates='user_orders')
    meals = db.relationship('OrdersMeals', back_populates='orders')


class Meal(db.Model):
    __tablename__ = 'meals'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    picture = db.Column(db.String)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('Category', back_populates='meals')
    orders = db.relationship('OrdersMeals', back_populates='meals')


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    meals = db.relationship('Meal', back_populates='category')
