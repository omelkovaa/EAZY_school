from flask import Blueprint, render_template, redirect, url_for, request, flash,session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db
from . import forms

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    form = forms.UsersLogin()
    return render_template('login.html', form=form)


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('emailField')
    password = request.form.get('passwordField')
    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    if user.username == 'admin':
        return redirect(url_for('admin.index'))

    login_user(user)
    return redirect(url_for('main.about'))


@auth.route('/signin')
def signup():
    form = forms.UsersReg()
    return render_template('signin.html', form=form)


@auth.route('/signin', methods=['POST'])
def signup_post():
    email = request.form.get('emailField')
    name = request.form.get('usernameField')
    native_language = request.form.get('native_languageField')
    password = request.form.get('passwordField')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.login'))

    print(email,name,native_language,password)

    new_user = User(email=email, username=name, native_language=native_language, password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    session["cart"] = []
    logout_user()
    return redirect(url_for('main.index'))