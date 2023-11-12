from flask import render_template, request, redirect, url_for, flash, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user, login_user, logout_user

from app import db, User

auth = Blueprint('auth', __name__)


@auth.route('/')
@auth.route('/index')
def index1():
    if current_user.is_anonymous:
        name = ''
    else:
        name = current_user.name  # <------- shows empty if left empty, how 'bout fixing it later, huh?
    return render_template('index.html', name=name)


@auth.route('/index2')
@login_required
def index2():
    return render_template('index2.html')


@auth.route('/index3')
def index3():
    return render_template('index3.html')


@auth.route('/profile')
@login_required
def profile():
    name = current_user.name
    return render_template('profile.html', name=name)


@auth.route("/exchange_rates")
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
    user = {'nickname': User.name}
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


@auth.route('/register')
def register_page():
    return render_template('register.html')


@auth.route('/register', methods=["GET", 'POST'])
def register():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    UserAttrib = 1
    user = User.query.filter_by(  # smth should be made about checking whether it is an existing email or not, somehow
        email=email).first()

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        return redirect(url_for('auth.register'))

        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'), UserAttrib=UserAttrib)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("auth.login"))  # <-------- make it login itself after registration


@auth.route('/login')
def login_page():
    return render_template('login.html')


@auth.route('/login', methods=["GET", 'POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if user is None or not check_password_hash(user.password, password):
        flash("Something does not quite come together. Either your input data is incorrect or ")
        return redirect((url_for('auth.login')))

    # login code goes here
    login_user(user, remember=remember)
    return redirect(url_for('auth.index1'))


# def login():
#  return render_template('test.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.index1'))
