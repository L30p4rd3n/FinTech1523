import datetime
from flask import Flask, render_template, send_from_directory
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
import time, apimoex, requests
import logging
from os import environ

db = SQLAlchemy()
scheduler = APScheduler()
# filename = f'/var/log/fp/{datetime.date} - fp.log

filename = f'{environ["VIRTUAL_ENV"]}/../logs/{datetime.date.today()} - fp.log'
logging.basicConfig(filename=filename,
                    level=logging.ERROR, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s',
                    filemode="a")

app = Flask(__name__)

app.config['SECRET_KEY'] = ''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hella_db.sqlite'
app.config['SCHEDULER_API_ENABLED'] = True
db.init_app(app)

scheduler.init_app(app)
scheduler.start()

login_manager = LoginManager()
login_manager.login_view = 'auth.login_page'
login_manager.init_app(app)


# logging.basicConfig()
# logging.getLogger('apscheduler').setLevel(logging.DEBUG)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64))
    login = db.Column(db.String(30))
    new_user = db.Column(db.Integer)
    user_advices = db.Column(db.String(1000))


class Advise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    adv = db.Column(db.String(1000))
    type = db.Column(db.Integer)

class AU(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer)
    aid = db.Column(db.Integer)


class Stocks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(100))
    ydate = db.Column(db.String(10))
    boardid = db.Column(db.String(5))
    dm1price = db.Column(db.Numeric(scale=3))
    dm2price = db.Column(db.Numeric(scale=3))
    dm3price = db.Column(db.Numeric(scale=3))
    dm4price = db.Column(db.Numeric(scale=3))
    dm5price = db.Column(db.Numeric(scale=3))
    dm6price = db.Column(db.Numeric(scale=3))
    dm7price = db.Column(db.Numeric(scale=3))


class SU(db.Model):  # Stock-User
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer)
    sid = db.Column(db.Integer)
    deleted = db.Column(db.Integer)


class Gstock(db.Model):  # Game-Stock
    id = db.Column(db.Integer, primary_key=True)
    bid = db.Column(db.Integer)
    name = db.Column(db.String(30))
    bcode = db.Column(db.String(5))
    date = db.Column(db.Integer)
    price = db.Column(db.Numeric(scale=3))
    risk = db.Column(db.Integer)


class UG(db.Model):  # User-Game
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer)
    day = db.Column(db.Integer)
    money = db.Column(db.Numeric(scale=3))
    salary = db.Column(db.Integer)
    tax = db.Column(db.Numeric(scale=3))
    risk = db.Column(db.Integer)
    zeal = db.Column(db.Integer)
    foresight = db.Column(db.Integer)
    worked = db.Column(db.Integer)


class UGS(db.Model):  # User-GameStock
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer)
    gsid = db.Column(db.Integer)
    amount = db.Column(db.Integer)

class bcreds(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cr1 = db.Column(db.String(75))
    cr2 = db.Column(db.String(75))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


from app.auth import auth as auth_blueprint

app.register_blueprint(auth_blueprint)

from app.api import api as api_blueprint

app.register_blueprint(api_blueprint)

from app.game import game as game_blueprint

app.register_blueprint(game_blueprint)


@app.errorhandler(404)
def error404(e):
    return render_template("r404.html"), 404


@app.errorhandler(500)
def e500(e):
    return {"Error": 500}


@scheduler.task('cron', id='flask_stock_reload', minute='0', hour='0')  # useless just now
def reload():
    for i in range(1, 13):
        with scheduler.app.app_context():
            stock = Stocks.query.filter_by(id=i).first()
            print(stock.boardid, stock.ydate)
            with requests.Session() as session:
                data = apimoex.get_board_history(session, stock.boardid, start=stock.ydate, end=stock.ydate)
                time.sleep(0.250)
                print(data)
            if len(data) == 0:
                print("none")
                continue
            else:
                dict_of_data = data[0]
                price = dict_of_data['CLOSE']
                stock.oneprice = price
                db.session.commit()


# scheduler.add_listener(reload)
@scheduler.task('cron', id='reload_log_file', minute='0', hour='0')
def newlog():
    logging.basicConfig(filename=filename,
                        level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


@app.route('/favicon.ico')
def favicon():
    import os
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == "__main__":
    app.run(host='127.0.0.1')
