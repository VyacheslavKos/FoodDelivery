import datetime

from functools import wraps

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask import flash
from flask import session
from flask import redirect
from flask import request
from flask import render_template
from flask import url_for

from app import app
from models import *
from forms import *

admin = Admin(app)

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Order, db.session))
admin.add_view(ModelView(Meal, db.session))
admin.add_view(ModelView(Category, db.session))


# Декоратор авторизации
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print("Нужно авторизоваться!")
        if not session.get('user_id'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.before_request
def before_request_func():
    if request.endpoint == 'admin' and not session.get('user_id'):
        return redirect(url_for('login'))


# Функция по формированию списка блюд в корзине
def cart_meals(meals):
    lst_meals = []
    if len(meals) > 0:
        for meal_id in meals:
            meal = Meal.query.get(meal_id)
            lst_meals.append(meal)
    return lst_meals


@app.route('/')
def main():
    cat_meals = {}
    lst_meals = cart_meals(session.get('cart', []))
    categories = Category.query.all()
    for category in categories:
        list_meal = []
        meals = Meal.query.filter_by(category_id=category.id).order_by(db.func.random()).all()
        for meal in meals:
            if len(list_meal) < 3:
                list_meal.append(meal)
        cat_meals[category.title] = list_meal
    return render_template('main.html', cat_meals=cat_meals, log=session.get('user_id', []), lst_meals=lst_meals)


@app.route('/addtocart/<int:meal_id>/')
def addtocart(meal_id):
    crt = session.get('cart', [])
    crt.append(meal_id)
    session['cart'] = crt
    return redirect(url_for('main'))


@app.route('/cart/', methods=["GET", "POST"])
def cart():
    form = OrderForm()
    lst_meals = cart_meals(session.get('cart', []))
    if session.get("user_id"):
        if request.method == "POST":
            if not form.validate_on_submit():
                form.errors.append("Не все поля заполнены корректно!")
                return render_template('cart.html', form=form, log=session.get('user_id'), lst_meals=lst_meals)

            user = User.query.get(session.get("user_id"))
            order = Order(date=datetime.datetime.today().strftime('%H:%M %d-%m-%Y'),
                          sum=form.order_summ.data,
                          status='preparing',
                          mail=user.mail,
                          phone=form.clientPhone.data,
                          address=form.clientAddress.data)
            db.session.add(order)

            meals = []
            for meal_id in session.get('cart'):
                if meal_id not in meals:
                    meals.append(meal_id)
                    db_meal = Meal.query.get(meal_id)
                    orders_meals = OrdersMeals(
                        meal_amount=session.get('cart').count(meal_id),
                        meal_sum=session.get('cart').count(meal_id) * int(db_meal.price),
                        orders=order,
                        meals=db_meal
                    )
                    db.session.add(orders_meals)

            db.session.commit()
            return redirect(url_for('ordered'))
    return render_template('cart.html', form=form, log=session.get('user_id', []), lst_meals=lst_meals)


@app.route('/delete/<int:meal_id>/')
def delete_meal(meal_id):
    crt = session.get('cart')
    crt.remove(meal_id)
    session['cart'] = crt
    meal = Meal.query.get(meal_id)
    flash(f"Блюдо {meal.title} удалено из корзины!")
    return redirect(url_for('cart'))


@app.route('/register/', methods=["GET", "POST"])
def register_():
    if session.get('user_id'):
        return redirect(url_for('main'))
    form = RegistrationForm()
    if request.method == "POST":
        if not form.validate_on_submit():
            return render_template("register.html", form=form)
        user = User.query.filter_by(mail=form.mail.data).first()
        if user:
            form.mail.errors.append("Пользователь с таким логином уже существует!")
            return render_template("register.html", form=form)
        user = User()
        user.mail = form.mail.data
        user.password_set(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f"Пользователь {form.mail.data} успешно зарегистрирован!")
        return redirect(url_for('register_'))
    return render_template("register.html", form=form)


@app.route('/login/', methods=["GET", "POST"])
def login():
    if session.get('user_id'):
        return redirect(url_for('main'))
    form = LoginForm()
    if request.method == "POST":
        if not form.validate_on_submit():
            return render_template("login.html", form=form)
        user = User.query.filter_by(mail=form.mail.data).first()
        if not user:
            form.mail.errors.append("Несуществующий логин")
        elif not user.password_valid(form.password.data):
            form.password.errors.append("Неверный пароль")
        else:
            session["user_id"] = user.id
            return redirect(url_for('account'))
    return render_template("login.html", form=form)


@app.route('/logout/')
@login_required
def logout():
    session.clear()
    return redirect(url_for('main'))


@app.route('/ordered/')
def ordered():
    session.pop('cart')
    return render_template('ordered.html')


@app.route('/account/')
def account():
    lst_meals = cart_meals(session.get('cart', []))
    user = User.query.get(session.get('user_id'))
    return render_template('account.html', user_orders=user.user_orders, log=session.get('user_id'),
                           lst_meals=lst_meals)
