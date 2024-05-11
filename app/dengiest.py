import decimal
import random
import sqlite3
from app.poker import play
from flask import render_template, request, Blueprint, current_app
from app import db, UG, UGS, Gstock
from flask_login import current_user
from os import environ

game = Blueprint("game", __name__, url_prefix="/game")


# f_news = open('news_of_the_day.txt')
# f_stocks = open('stocks.txt')
# news_of_the_day = []
# stocks = []
# user_stocks = []
# for line in f_news:
#    news_of_the_day.append(line)
#
# for line in f_stocks:
#    stocks.append(list(line.split("|")))
#    a = list(line.split("|"))
#    a.append(" 0")
#    user_stocks.append(a)


@game.route('/test')
def load_vari():
    return render_template("game.html")


@game.route('/test', methods=["get", "post"])
def vari():
    user = UG.query.filter_by(uid=current_user.id).first()
    zeal, foresight, risky = user.zeal, user.foresight, user.risk

    v = request.get_data()
    if v == b'1':
        if not user.worked:
            user.zeal += 1
            db.session.commit()
        return "/game/skip"
    elif v == b'2':
        return "/game/check"
    elif v == b'3':
        foresight += 1
        return "/game/buy"
    elif v == b'4':
        return "/game/sell"
    elif v == b'5':
        return "/game/next"
    elif v == b'6':
        risky += 1
        return "/game/rps"
    elif v == b'7':
        risky += 1
        return "/game/poker"
    else:
        return " ", 400


@game.route("/g", methods=["POST"])
def give_info():
    user = UG.query.filter_by(uid=current_user.id).first()
    day, money, salary = user.day, user.money, user.salary
    stocks = [i.price for i in Gstock.query.filter_by(date=day).all()]
    return {
        "day": day,
        "money": money,
        "salary": salary,
        "stocks": stocks
    }


@game.route("/next", methods=["POST"])
def new_day():
    user = UG.query.filter_by(uid=current_user.id).first()
    day, money, salary = user.day, user.money, user.salary

    user.money += decimal.Decimal(salary)
    user.day += 1
    day += 1
    user.worked = 0

    db.session.commit()
    return {
        "day": day,
        "money": money,
    }


@game.route('/skip', methods=["post"])
def skip():
    user = UG.query.filter_by(uid=current_user.id).first()

    day, money, salary = user.day, user.money, user.salary
    user.money += decimal.Decimal(salary * 1.5)

    result = {"success": 0,
              "salary": user.salary}

    if random.random() > 0.7 and user.worked != 1:
        user.salary *= 1.5
        user.worked = 1
        result["success"] = 1
    elif user.worked == 1:
        return "", 200

    db.session.commit()
    return result


@game.route('/check', methods=["POST"])
def check_stock():
    user = UG.query.filter_by(uid=current_user.id).first()
    user_stocks = UGS.query.filter_by(uid=current_user.id).all()
    quantities = [i.amount for i in user_stocks]

    prices = []
    gsids = [i.gsid for i in user_stocks]
    names = []

    conn = sqlite3.connect(f'{environ["VIRTUAL_ENV"]}/../instance/hella_db.sqlite')
    # conn = sqlite3.connect(f'{environ["VIRTUAL_ENV"]}/var/app-instance/hella_db.sqlite')

    c = conn.cursor()
    for i in range(len(gsids)):
        c.execute(f"SELECT * FROM Gstock WHERE date={user.day} AND bid={gsids[i]}")
        res = c.fetchone()
        if quantities[i]:
            prices.append(float(format(res[-2] * quantities[i], '.3f')))
            names.append(res[-5])

    response = {"names": names,
                "amounts": [],
                "prices": prices}

    for i in range(len(quantities)):
        if quantities[i] != 0:
            response["amounts"].append(quantities[i])

    if not response["amounts"]:
        return {}, 204

    conn.close()

    return response, 200


@game.route('/buy', methods=["POST"])  # TODO POST -> PUT
# TODO ВАЖНО - ПРИ ВЫЗОВЕ buy() !!!НА ФРОНТЕ!!! ВЫЗВАТЬ check(), А ЗАТЕМ buy()
def buy():
    user = UG.query.filter_by(uid=current_user.id).first()
    day = user.day
    __data__ = request.get_json()
    num, cnt = __data__["num"], __data__["count"]
    try:
        num, cnt = int(num), int(cnt)
    except ValueError:
        current_app.logger.error("Invalid data in function %s: %s, %s", "buy", num, cnt)
        return "", 400

    conn = sqlite3.connect(f'{environ["VIRTUAL_ENV"]}/../instance/hella_db.sqlite')  # that sucks
    # conn = sqlite3.connect("/var/www/scproj/scproj/var/app-instance/hella_db.sqlite")
    c = conn.cursor()
    c.execute(f"SELECT * FROM Gstock WHERE date={day} AND bid={num}")
    a = c.fetchone()
    try:
        if num < 0 or num > 10:
            return "", 400
        elif a[5] * cnt > user.money:
            return "", 204
    except ValueError:
        return "", 400
    try:
        res = c.execute(f"SELECT * FROM UGS WHERE gsid={a[1]} AND uid={current_user.id}")
        if res.fetchone() is None:
            bstock = UGS(uid=current_user.id, gsid=a[1], amount=cnt)
            db.session.add(bstock)
        else:
            c.execute(f"""
                UPDATE UGS
                SET amount = amount + {cnt}
                WHERE uid = {current_user.id} and gsid={num};
                """)
            user.money -= decimal.Decimal(a[5] * cnt)
    except sqlite3.Error as error:
        conn.rollback()
        db.session.rollback()
        current_app.logger.error("Error:", error)
        return ":(", 500

    finally:
        conn.commit()
        db.session.commit()
        conn.close()
    return "", 200


@game.route("/sell", methods=["POST"])  # TODO POST -> PATCH/DELETE
def sell():  # TODO - снова, запрос на check(), потом сюда
    user = UG.query.filter_by(uid=current_user.id).first()
    day = user.day
    __data__ = request.get_json()
    num, cnt = __data__["num"], __data__["count"]  # num - id акции, cnt - кол-во

    try:
        num, cnt = int(num), int(cnt)
    except ValueError:
        current_app.logger.error("Invalid data in function %s: %s, %s", "sell", num, cnt)
        return "", 400

    conn = sqlite3.connect(f'{environ["VIRTUAL_ENV"]}/../instance/hella_db.sqlite')
    # conn = sqlite3.connect("/var/www/scproj/scproj/var/app-instance/hella_db.sqlite")
    c = conn.cursor()
    c.execute(f"SELECT * FROM Gstock WHERE date={day} AND bid={num}")
    a = c.fetchone()
    try:
        if num < 0 or num > 10:
            return "", 400
    except ValueError:
        return "", 400

    try:
        _res_ = c.execute(f"SELECT * FROM UGS WHERE gsid={a[1]} AND uid={current_user.id}")
        res = _res_.fetchone()
        if res is None:
            current_app.logger.error("User %s, id %s: Can't update stocks: stock not found.",
                                     current_user.login, current_user.id)
            return "", 404
        else:
            if cnt > res[-1]:
                current_app.logger.error("User %s, id %s: Can't update stocks: %s > %s",
                                         current_user.login, current_user.id, cnt, res[-1])
                return "", 400

            c.execute(f"""
                    UPDATE UGS
                    SET amount = amount - {cnt}
                    WHERE uid = {current_user.id} and gsid={num};
                    """)
            user.money += decimal.Decimal(a[5] * cnt)
    except sqlite3.Error as error:
        conn.rollback()
        db.session.rollback()
        current_app.logger.error("Error:", error)
        return ":(", 500

    finally:
        conn.commit()
        db.session.commit()
        conn.close()
    return "", 200


@game.route("/rps", methods=["POST"])
def rock_paper_scissors_game():
    user = UG.query.filter_by(uid=current_user.id).first()
    data = request.get_json()

    user_choice, user_bet = data["num"], data["count"]

    try:
        user_choice, user_bet = int(data["num"]), float(data["count"])
        if user_choice > 3:
            return "", 400
        if user_bet < 0 or user_bet > user.money:
            return "", 400
    except ValueError:
        current_app.logger.error("Invalid data in function %s: %s, %s", "rps", user_choice, user_bet)
        return "", 400

    bot_choice = random.choice([1, 2, 3])  # rock, paper, scissors == 1, 2, 3

    if user_choice == bot_choice:
        user.money -= decimal.Decimal(user_bet)
        db.session.commit()
        return {
            "user": user_choice,
            "bot": bot_choice,
            "won": 0
        }
    elif (user_choice == 1 and bot_choice == 2) or (
            user_choice == 2 and bot_choice == 3) or (
            user_choice == 3 and bot_choice == 1):
        user.money += decimal.Decimal(user_bet)
        db.session.commit()
        return {
            "user": user_choice,
            "bot": bot_choice,
            "won": 1
        }
    else:
        user.money -= decimal.Decimal(user_bet)
        db.session.commit()
        return {
            "user": user_choice,
            "bot": bot_choice,
            "won": 0
        }


# while (day < 31):
#    new_Day()
# вынести на фронт этот while

@game.route("/poker", methods=["POST"])
def poker():
    user = UG.query.filter_by(uid=current_user.id).first()
    # print("Давай сыграем в покер")
    # print("Сколько хочешь поставить?")
    user_bet = request.get_data()
    try:
        user_bet = int(user_bet)
    except ValueError:
        current_app.logger.error("Invalid data in function %s: %s", "poker", user_bet)
        return "", 400
    data = play()
    if data["playerwon"]:
        user.money += user_bet
    else:
        user.money -= user_bet
    db.session.commit()
    return dict(data)
