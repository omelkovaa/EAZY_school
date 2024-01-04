from flask_wtf import FlaskForm
from wtforms import Form, SubmitField, StringField, validators, FloatField, PasswordField, BooleanField
from flask_wtf.file import FileField,FileRequired,FileAllowed


class UsersLogin(FlaskForm):
    emailField = StringField('email', [validators.Length(min=6, max=35)])
    passwordField = PasswordField('Пароль', [validators.Length(min=6, max=35)])
    submit = SubmitField('Войти')


class UsersReg(FlaskForm):
    usernameField = StringField('Имя', [validators.Length(min=1)])
    emailField = StringField('email', [validators.Length(min=6, max=35)])
    passwordField = PasswordField('Пароль', [validators.Length(min=6, max=35)])
    native_languageField = StringField('native_language', [validators.Length(min=1)])
    submit = SubmitField('Зарегистрироваться')


class UserSub(FlaskForm):
    usernameField = StringField('Имя', [validators.Length(min=1)])
    emailField = StringField('email', [validators.Length(min=6, max=35)])
    submit = SubmitField('Отправить')