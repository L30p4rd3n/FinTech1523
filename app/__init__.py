from flask import Flask, render_template, redirect, flash, request
import os

# from wtforms import Form, BooleanField, StringField, PasswordField, validators
# from wtforms.validators import DataRequired
from app import forms
from app import db

# class LoginForm(Form):
#    username = StringField('Username', [validators.Length(min=4, max=25)])
#    remember_me = BooleanField('Remember this name', default=False)
# email = StringField('Email Address', [validators.Length(min=6, max=35)])
# password = PasswordField('New Password', [
#    validators.DataRequired(),
#    validators.EqualTo('confirm', message='Passwords must match')
# ])
# confirm = PasswordField('Repeat Password')
# accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])
# class ChangePassword(Form):
# password = PasswordField('New Password', [InputRequired(), EqualTo('confirm', message='Passwords must match')])
# confirm  = PasswordField('Repeat Password')


def get_values():
    import requests
    from bs4 import BeautifulSoup
    import re

    link = 'https://www.cbr.ru/'
    requests.get(link)
    page = BeautifulSoup(requests.get(link).text, 'html.parser')
    values = page.find_all('div', class_='col-md-2 col-xs-9 _right mono-num')
    prices = [1, 2, 3]
    price1 = ''
    price2 = ''
    price3 = ''

    for i in range(len(values)):
        prices.append(values[i].text)
        prices[i] = re.sub(r"[\n\t\s]*", "", prices[i])
        price1 = f"Yuan - {prices[0:2]} buy/sell"
        price2 = f"Dollar - {prices[2:4]} buy/sell"
        price3 = f"Euro - {prices[4:-1]} buy/sell"
        prices = [price1, price2, price3]
    return price1, price2, price3


app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='123',
    DATABASE=os.path.join(app.instance_path, 'somedb.sqlite'),
)  # hui poimet kak rabotaet


@app.route("/")
@app.route("/start")
def main_menu():  # можно сунуть в отдельный файл
    user = {'nickname': 'asda'}
    post = [
        {
            'value': {'currency': 'Yuan'},
            'body': "price1"  # видимо, необходимо заполнение из базы данных.
        },
        {
            'value': {'currency': 'Dollar'},
            'body': "price2"
        },
        {
            'value': {'currency': 'Euro'},
            'body': "price3"
        }
    ]
    return render_template("mainmenu.html",
                           title='a',
                           user=user,
                           post=post)


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!проверить установленные библиотеки, поставить, если что где нужно(по учебнику)!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
@app.route('/test/', methods=['POST', 'GET'])
def test():
    message = ''
    username = request.form.get('username')  # запрос к данным формы
    password = request.form.get('password')
    #user_id = 0
    #if username:      # not working
    #    user_id += 1;
    #    db.c.execute(f"""
    #INSERT INTO data_from_form VALUES
    #    ({user_id},{username}),
    #    """)
    if username == 'root' and password == 'pass':  # captcha-database could work like this: we take a pic ind a key for
        # it to display on screen
        message = "Correct username and password"
        return redirect('/start')
    else:
        message = 'a' # define the way to not get to False at any circumstances


    return render_template('test.html', message=message)
