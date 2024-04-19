import flask
from flask import render_template, request, redirect, url_for, flash, Blueprint, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user, login_user, logout_user
import random

from app import db, User, Advise, Stocks

auth = Blueprint('auth', __name__)


@auth.route('/')
@auth.route('/index')
def index1():
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
        if int(current_user.is_risky) > 55:
            soveti = Advise.query.filter_by(adv_type='1').all()
            for i in range(3):
                flash(soveti[i].adv)
        else:
            soveti = Advise.query.filter_by(adv_type='2').all()
            for i in range(3):
                flash(soveti[i].adv)
        if int(current_user.invest) > 75:
            soveti = Advise.query.filter_by(adv_type='3').all()
            for i in range(3):
                flash(soveti[i].adv)
        else:
            soveti = Advise.query.filter_by(adv_type='4').all()
            for i in range(3):
                flash(soveti[i].adv)
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
    new_user = User(email=email, login=login, password=generate_password_hash(password), new_user=0,
                    is_risky=0, invest=0)
    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)

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
