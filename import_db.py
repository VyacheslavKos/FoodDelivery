import csv

from flask import Flask

from config import Config
from models import Category, Meal
from app import db


ctx = Flask(__name__)
ctx.config.from_object(Config)
db.init_app(ctx)
ctx.app_context().push()

with open('./data/delivery_categories.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    categories = list(reader)

with open('./data/delivery_items.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    meals = list(reader)


def seed():
    for category1 in categories:
        category = Category(
            title=category1['title']
        )
        db.session.add(category)

    for meal1 in meals:
        meal = Meal(
            title=meal1['title'],
            price=int(meal1['price']),
            description=meal1['description'],
            picture=meal1['picture'],
            category_id=int(meal1['category_id'])
        )
        db.session.add(meal)
    db.session.commit()


if __name__ == '__main__':
    seed()
