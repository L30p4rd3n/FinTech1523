from flask import Flask, render_template, abort
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
from sqlalchemy.ext.declarative import declarative_base
import time, apimoex, requests

# import logging

db = SQLAlchemy()
scheduler = APScheduler()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'aGRjZmRzNDIzMzRmc2QzNDemZnMTIzZGY'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hella_db.sqlite'
app.config['SCHEDULER_API_ENABLED'] = True
db.init_app(app)

scheduler.init_app(app)
scheduler.start()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


# logging.basicConfig()
# logging.getLogger('apscheduler').setLevel(logging.DEBUG)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64))
    login = db.Column(db.String(30))
    # UserAttrib = db.Column(db.Integer)  # could possibly be changed to a list of links??
    new_user = db.Column(db.Integer)
    is_risky = db.Column(db.Integer)
    invest = db.Column(db.Integer)
    user_advices = db.Column(db.String(1000))
    # how 'bout making a separate database to take the links from for filling?


class Advise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    adv_type = db.Column(db.Integer)
    adv = db.Column(db.String(1000))


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


class AU(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer)
    aid = db.Column(db.Integer)


class SU(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer)
    sid = db.Column(db.Integer)
    deleted = db.Column(db.Integer)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


from app.auth import auth as auth_blueprint

app.register_blueprint(auth_blueprint)

from app.api import api as api_blueprint

app.register_blueprint(api_blueprint)


@app.errorhandler(404)
def error404(e):
    return render_template("r404.html")



@scheduler.task('cron', id='flask_stock_reload', minute='0', hour='0')
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
                print("NOOOOOOONEEEEEEE")
                continue
            else:
                dict_of_data = data[0]
                price = dict_of_data['CLOSE']
                stock.oneprice = price
                db.session.commit()


# scheduler.add_listener(reload)

if __name__ == "__main__":
    app.run(host='127.0.0.1')
