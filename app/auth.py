import flask
from flask import render_template, request, redirect, url_for, Blueprint, abort, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user, login_user, logout_user
import random

from app import db, User, Advise, UG, AU

auth = Blueprint('auth', __name__)


@auth.route('/')
@auth.route('/index')
def index1():
    if current_user.is_anonymous:
        return render_template("index.html", login='')
    else:
        login = current_user.login
        if current_user.new_user == 0:
            return render_template('index1.html', login=login) # прошел игру, советы
        elif current_user.new_user == 2:
            return render_template('index2.html', login=login)  # недопрошел игру
    return render_template('index.html', login=login) # не прошел игру

@auth.route('/getadv', methods=["post"])
@login_required
def getadv():
    advices = []
    try:
        advices = [i.aid for i in AU.query.filter_by(uid=current_user.id).all()]
        for i in range(len(advices)):
            a = Advise.query.filter_by(id=advices[i]).first()
            advices[i] = a.adv
    except Exception:
        advices = []
        current_app.logger.error(Exception)
    return {"msg": advices}, 200

@auth.route('/profile')
@login_required
def profile():
    login = current_user.login
    return render_template("profile.html", login=login)


@auth.route('/register')
def register_page():
    return render_template('register.html')


@auth.route('/register/r', methods=['POST'])
def register():
    udata = request.get_json()
    email = udata["email"]
    login = udata["login"]
    password = udata["password"]

    user = User.query.filter_by(email=email).first()
    _user = User.query.filter_by(login=login).first()
    if user or _user:
        return "", 400

    new_user = User(email=email, login=login, password=generate_password_hash(password), new_user=1)

    current_app.logger.info("%s, %s registered.", email, login)  # wow
    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)

    ug_profile = UG(uid=current_user.id, day=1, money=5, salary=15000, tax=0.185, risk=0, zeal=0, foresight=0, worked=0)
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
@auth.route("/gamebutt")
@login_required
def gamebuttheh():
    return render_template("gamebutt.html")
# def login():
#  return render_template('test.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.index1'))


#@auth.route('/send')
#def viewapi():
#    return render_template("send.html")
# - removed because test
