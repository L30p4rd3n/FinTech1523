from flask import Flask, render_template, redirect, request, url_for, current_app, flash
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from app import forms

app = Flask(__name__)

app.config['SECRET_KEY'] = 'qwert'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hella_db.sqlite'

db = SQLAlchemy()

db.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


login_manager = LoginManager()
login_manager.login_view = '/login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/')
@app.route('/index')
def index1():
    return render_template('index.html')


@app.route('/index2')
def index2():
    return render_template('index2.html')


@app.route('/index3')
def index3():
    return render_template('index3.html')


@app.route("/exchange_rates")
def exchange_rates():  # можно сунуть в отдельный файл
    import requests
    from bs4 import BeautifulSoup
    import re

    link = 'https://www.cbr.ru/'
    requests.get(link)
    page = BeautifulSoup(requests.get(link).text, 'html.parser')
    values = page.find_all('div', class_='col-md-2 col-xs-9 _right mono-num')
    prices = []
    ''
    ''
    ''

    for i in range(len(values)):
        prices.append(values[i].text)
        prices[i] = re.sub(r"[\n\t\s]*", "", prices[i])
    price1 = f"{prices[0] + ' ' + prices[1]} buy/sell".replace('[]', '')
    price2 = f"{prices[2] + ' ' + prices[3]} buy/sell".replace('[]', '')
    price3 = f"{prices[4] + ' ' + prices[5]} buy/sell".replace('[]', '')
    user = {'nickname': 'asda'}
    post = [
        {
            'value': {'currency': 'Yuan, CNY'},
            'body': price1  # видимо, необходимо заполнение из базы данных.
        },
        {
            'value': {'currency': 'Dollar, USD'},
            'body': price2
        },
        {
            'value': {'currency': 'Euro, EUR'},
            'body': price3
        }
    ]
    return render_template("exchange_rates.html",
                           title='a',
                           user=user,
                           post=post)


@app.route('/register', methods=["GET", 'POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(
        email=email).first()  # if this returns a user, then the email already exists in database

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        return redirect(url_for('/signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect('login')  # might have to do different one here

@app.route('/login', methods=["GET", 'POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect('/register')  # if the user doesn't exist or password is wrong, reload the page
 #login code goes here
# login_user(user, remember=remember)
    return redirect('/')
 #def login():
 #  return render_template('test.html')
