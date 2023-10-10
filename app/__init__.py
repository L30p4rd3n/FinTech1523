from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])


def get_values():
    import requests
    from bs4 import BeautifulSoup
    import re
    global fin_prices

    link = 'https://www.cbr.ru/'
    requests.get(link)
    page = BeautifulSoup(requests.get(link).text, 'html.parser')
    values = page.find_all('div', class_='col-md-2 col-xs-9 _right mono-num')
    prices = []

    for i in range(len(values)):
        prices.append(values[i].text)
        prices[i] = re.sub(r"[\n\t\s]*", "", prices[i])
        price1 = f"Yuan - {prices[0:2]} buy/sell"
        price2 = f"Dollar - {prices[2:4]} buy/sell"
        price3 = f"Euro - {prices[4:-1]} buy/sell"
        fin_prices = [price1, price2, price3]
    return 0


app = Flask(__name__)
app.config.from_object('config')


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


@app.route('/submit')
def submit(methods=['GET', 'POST']):
    form = MyForm()
    if form.validate_on_submit():
        return redirect('/home')
    return render_template('form.html', form=form)
