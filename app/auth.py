import flask
from flask import render_template, request, redirect, url_for, flash, Blueprint, abort, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user, login_user, logout_user
import random

from app import db, User, Advise, Stocks, UG, UGS

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
        return redirect("/game/test")


@auth.route('/register')
def register_page():
    return render_template('register.html')


@auth.route('/register/r', methods=['POST'])
def register():
    udata = request.get_json()
    print(udata)
    email = udata["email"]
    login = udata["login"]
    password = udata["password"]

    #SSTI?

    user = User.query.filter_by(email=email).first()
    if user:
        return "", 400
        #return redirect(url_for('auth.register'))

    new_user = User(email=email, login=login, password=generate_password_hash(password), new_user=1)

    current_app.logger.info("%s, %s registered.", email, login)  # wow
    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)

    ug_profile = UG(uid=current_user.id, day=1, money=0, salary=15000, tax=0.130, risk=0, zeal=0, foresight=0, worked=0)
    db.session.add(ug_profile)
    db.session.commit()

    return redirect("/")


@auth.route("/login")
def login_page():
    return render_template("login.html")


@auth.route('/login/check', methods=["POST"])
def check_passwd():
    udata = request.get_json()
    login = udata["login"]
    password = udata["password"]
    remember = udata["remember"]
    user = User.query.filter_by(login=login).first()
    if not user or not check_password_hash(user.password, password):
        abort(401)
    # login code goes here
    login_user(user, remember=remember)
    check_db = UG.query.filter_by(uid=user.id).first()
    if check_db is None:
        ug_profile = UG(uid=current_user.id, day=1, money=0, salary=15000, tax=0.130, risk=0, zeal=0, foresight=0,
                        worked=0)
        db.session.add(ug_profile)
        db.session.commit()

    return "", 200


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
