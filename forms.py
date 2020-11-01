from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length, EqualTo, InputRequired, Email


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
