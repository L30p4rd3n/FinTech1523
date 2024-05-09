import decimal
import random
import sqlite3
import time
from app.poker import play
import flask
from flask import render_template, request, redirect, url_for, flash, Blueprint, abort, current_app
from app import db, User, Advise, Stocks, SU, UG, UGS, Gstock
from flask_login import login_required, current_user, logout_user, login_user
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
    money, tax, salary = user.money, user.tax, user.salary

    # print("Как насчет поработать еще пару часиков? За целых 1,5 зарплаты? Введи 1!")
    # print("Посмотреть свои акции? Введи 2!")
    # print("Инвестировать? Введи 3!")
    # print("Продашь акции? Введи 4!")
    # print("Сыграем? Введи 5!")

    # должно быть в меню, которое видно на ВСЕХ устройствах

    v = request.get_data()
    if (v == b'1'):
        zeal += 1
        if user.worked:
            return " ", 204
        else:
            return "/game/skip"
    elif (v == b'2'):
        return "/game/check"
    elif (v == b'3'):
        foresight += 1
        return "/game/buy"
    elif (v == b'4'):
        return "/game/sell"
    elif (v == b'5'):
        risky += 1
        print("Давай сыграем в покер")
        print("Сколько хочешь поставить?")
        stavka = int(input())
        if (play()):
            money += stavka
        else:
            money -= stavka
    elif v == b'6':
        return "/game/next"
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
def new_Day():
    user = UG.query.filter_by(uid=current_user.id).first()
    day, money, salary = user.day, user.money, user.salary

    user.money += decimal.Decimal(salary)
    user.day += 1  # everything else is on frontend, cuz idgaf and stfu.
    day += 1
    user.worked = 0

    # stock_change()
    db.session.commit()
    # print(f"Сегодня {day} день, а у вас на счёте {money} рублей")
    # print(news_of_the_day[day - 1]) # TODO news_of_the_day сделать через взятие акций за день в stock_change() и фронт
    # todo - проверка на наличие денег(no debt?), а хотя, стоит ли? Или сделать выполнимость 100%?

    return {
        "day": day,
        "money": money,
    }

@game.route('/skip', methods=["post"])
def skip():
    user = UG.query.filter_by(uid=current_user.id).first()
    user.worked = 1
    day, money, salary = user.day, user.money, user.salary
    user.money += decimal.Decimal(salary * 1.5)
    db.session.commit()
    if (random.random() > 0.7):  # and day > 10):
        user.salary *= 1.5
        db.session.commit()
        return {"success": 1,
                "salary": user.salary}
    else:
        return {"success": 0,
                "salary": salary}


@game.route('/check', methods=["POST"])
def check_stock():
    user = UG.query.filter_by(uid=current_user.id).first()
    user_stocks = UGS.query.filter_by(uid=current_user.id).all()
    quantities = [i.amount for i in user_stocks]

    prices = []
    gsids = [i.gsid for i in user_stocks]
    names = []

    conn = sqlite3.connect(f'{environ["VIRTUAL_ENV"]}/../instance/hella_db.sqlite')
    # conn = sqlite3.connect("/var/www/scproj/scproj/var/app-instance/hella_db.sqlite")

    c = conn.cursor()
    for i in range(len(gsids)):
        c.execute(f"SELECT * FROM Gstock WHERE date={user.day} AND bid={gsids[i]}")
        res = c.fetchone()
        if quantities[i]:
            prices.append(float(format(res[-2] * quantities[i], '.3f')))
            names.append(res[-5])

    response = {"names":names,
                "amounts":[],
                "prices":prices}

    for i in range(len(quantities)):
        if quantities[i] != 0:
            response["amounts"].append(quantities[i])

    if response["amounts"] == []:
        return {}, 204

    conn.close()

    return response, 200



@game.route('/buy', methods=["POST"]) # TODO POST -> PUT
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


@game.route("/sell", methods=["POST"]) # TODO POST -> PATCH/DELETE
def sell():  # TODO - снова, запрос на check(), потом сюда
    user = UG.query.filter_by(uid=current_user.id).first()
    user_stocks = UGS.query.filter_by(uid=current_user.id).all()
    global money
    number = 1
    # for i in user_stocks:
    #    print(number, " | ", "|".join(i))
    # print("-" * 20)
    # print("Введите номер акции которую хотите продать")
    # num = int(input())
    day = user.day
    __data__ = request.get_json()
    num, cnt = __data__["num"], __data__["count"]  # num - id акции, cnt - кол-во
    try:
        num, cnt = int(num), int(cnt)
    except ValueError:
        current_app.logger.error("Invalid data in function %s: %s, %s", "sell", num, cnt)
        return "", 400

    conn = sqlite3.connect(f'{environ["VIRTUAL_ENV"]}/../instance/hella_db.sqlite')  # that sucks
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


def rock_paper_scissors_game():
    global money
    # print("Введите ставку") - дело фронта.
    bet = 0
    user_choice = input('Введите ваш выбор (Камень, Ножницы, Бумага): ')
    choices = ['Камень', 'Ножницы', 'Бумага']

    # Random Bot Choice
    bot_choice = random.choice(choices)

    # Game Logic

    # 1 - Победа игрока; 2 - победа бота, 3 - ничья

    if user_choice == bot_choice:
        return 3
    elif (user_choice == 'Камень' and bot_choice == 'Ножницы') or (
            user_choice == 'Ножницы' and bot_choice == 'Бумага') or (
            user_choice == 'Бумага' and bot_choice == 'Камень'):
        return f'Вы выиграли! Вы выбрали {user_choice}, бот выбрал {bot_choice}'
    else:
        return f'Вы проиграли! Бот выбрал {bot_choice}, вы выбрали {user_choice}'

# while (day < 31):
#    new_Day()
#### вынести на фронт этот while
