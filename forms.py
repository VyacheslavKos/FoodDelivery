from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms import SubmitField
from wtforms import HiddenField
from wtforms.validators import DataRequired
from wtforms.validators import Length
from wtforms.validators import EqualTo
from wtforms.validators import InputRequired
from wtforms.validators import Email


class OrderForm(FlaskForm):
    clientName = StringField("Ваше имя", validators=[InputRequired()])
    clientAddress = StringField("Ваш адрес", validators=[InputRequired()])
    clientPhone = StringField("Ваш номер телефона", validators=[InputRequired()])
    order_summ = HiddenField()
    submit = SubmitField('Оформить заказ')


class LoginForm(FlaskForm):
    mail = StringField("Логин (электронная почта)", validators=[Email(message="Неверный формат почты!")])
    password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    mail = StringField("Введите логин (электронная почта)", validators=[DataRequired(),
                                                                        Email(message="Неверный формат почты!")])
    password = PasswordField(
        "Введите пароль",
        validators=[
            DataRequired(),
            Length(min=5, message="Пароль должен быть не менее 5 символов!"),
            EqualTo('confirm_password', message="Пароли не одинаковые!")
        ]
    )
    confirm_password = PasswordField("Продублируйте пароль")
    submit = SubmitField('Зарегистрироваться')
