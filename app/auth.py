import flask
from flask import render_template, request, redirect, url_for, flash, Blueprint, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user, login_user, logout_user
import random

from app import db, User, Advise, Stocks, UG

auth = Blueprint('auth', __name__)


@auth.route('/')
@auth.route('/index')
def index1():
    agent_string = request.user_agent.string
    if current_user.is_anonymous:
        login = ''
    else:
        login = current_user.login
    return render_template('index.html', login=login)


@auth.route('/profile')
@login_required
def profile():
    is_new = current_user.new_user
    login = current_user.login
    if is_new == 0:
        return render_template("profile.html", login=login)
    else:
        return render_template("gamebutt.html", login=login)


@auth.route('/register')
def register_page():
    return render_template('register.html')


@auth.route('/register', methods=["GET", 'POST'])
def register():
    email = request.form.get('email')
    login = request.form.get('login')
    password = request.form.get('password')
    if password == '' or login == '' or password == '':
        flash("Остались незаполненные поля. Просим отправить данные заново, заполнив все поля")  # ебнуть js и REST?

        return redirect("/register")
    user = User.query.filter_by(email=email).first()

    if user:
        flash("Данный пользователь уже существует.")
        return redirect(url_for('auth.register'))
    new_user = User(email=email, login=login, password=generate_password_hash(password), new_user=0)
    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)

    ug_profile = UG(uid=current_user.id, day=0, money=0, salary=15000, tax=0.130, risk=0, zeal=0, foresight=0)
    db.session.add(ug_profile)
    db.session.commit()

    return redirect("/")


@auth.route("/login")
def login_page():
    return render_template("login.html")



@auth.route('/test')
def test_page():
    return render_template('test.html')


@auth.route('/game')
@login_required
def game_page():
    if current_user.new_user == 0:
        return redirect('/profile')
    return render_template('game.html', login=current_user.login)


# def login():
#  return render_template('test.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.index1'))


@auth.route('/send')
def viewapi():
    return render_template("send.html")
