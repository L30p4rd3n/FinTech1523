import random
import sqlite3
import time
from app.poker import play
import flask
from flask import render_template, request, redirect, url_for, flash, Blueprint, abort, current_app
from app import db, User, Advise, Stocks, SU, UG, UGS, Gstock
from flask_login import login_required, current_user, logout_user, login_user

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
    return render_template("send.html")


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
        return redirect('/game/skip', 307)
    elif (v == b'2'):
        return redirect("/game/check", 307)
        # return vari() # yeet that infinite recursion outta here?
    elif (v == b'3'):
        foresight += 1
        return buy()
    elif (v == b'4'):
        pass
        # sell()
    elif (v == b'5'):
        risky += 1
        print("Давай сыграем в покер")
        print("Сколько хочешь поставить?")
        stavka = int(input())
        if (play()):
            money += stavka
        else:
            money -= stavka
    else:
        return " ", 204


def new_Day():
    user = UG.query.filter_by(uid=current_user.id).first()
    day, money, salary = user.day, user.money, user.salary
    user.money += salary
    user.day += 1  # everything else is on frontend, cuz idgaf and stfu.
    # stock_change()
    db.session.commit()
    # print(f"Сегодня {day} день, а у вас на счёте {money} рублей")
    # print(news_of_the_day[day - 1]) # TODO news_of_the_day сделать через взятие акций за день в stock_change() и фронт
    # todo - проверка на наличие денег(no debt?), а хотя, стоит ли? Или сделать выполнимость 100%?
    return {
        "day": day,
        "money": money
    }


@game.route('/skip', methods=["post"])
def skip():
    user = UG.query.filter_by(uid=current_user.id).first()
    day, money, salary = user.day, user.money, user.salary
    user.money += salary * 1.5
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
    user_stocks = UGS.query.filter_by(uid=current_user.id).first()
    if user_stocks:
        send = {"data": []}
        for i in range(len(user_stocks)):
            send["data"].append(user_stocks[i])
        return send
    err = ("У вас нет купленных лотов.")
    return flask.jsonify({"text": err}), 204  # JSON for equal-type return.


@game.route('/buy', methods=["POST"])
# ВАЖНО - ПРИ ВЫЗОВЕ buy() !!!НА ФРОНТЕ!!! ВЫЗВАТЬ check(), А ЗАТЕМ buy()
def buy():
    stocks = Gstock.query.all()
    user = UG.query.filter_by(uid=current_user.id).first()
    money = user.money
    user_stocks = UGS.query.filter_by(uid=current_user.id).all()
    # for i in stocks: # STOP PUTTING for i in SOMETHING!!! PLS USE for i in range(len(SOMETHING)) D;
    # print("Введите номер акции которую хотите приобрести")
    try:
        __data__ = request.get_json()
        num, cnt = int(__data__["num"], __data__["count"])
        #price = Gstock. # TODO - some shitfuck in there + gstock 1 -> 31 days - fixed state
    except ValueError:
        return " ", 400
    # print("Введите количество акций которые вы хотите приобритсти")
    # count = int(input())
    if (num < 0 or num > 11):
        return " ", 400
        # ch = int(input())
        # if ch == 1:
        #    return 0
    # if (count * int(stocks[num - 1][1]) < money):
    #    user_stocks[num - 1][3] = " " + str(int(user_stocks[num - 1][3]) + count)
    #    print(f"Вы успешно купили {count} лотов акций", "".join(user_stocks[num - 1][0]))
    # else:
    #    print("Недостаточно денег.")
    return str(type(num))


# def stock_change():
#    for i in user_stocks:
#        if (int(i[3]) > 0):
#            pr = int(list(i[2].split("%"))[0])
#            pr = 1.1 - pr / 100
#            if (random.random() < pr):
#                i[1] = str(int(i[1]) + int(i[1]) * int(list(i[2].split("%"))[0]) // 100)
#

# def sell():
#    global money
#    number = 1
#    for i in user_stocks:
#        print(number, " | ", "|".join(i))
#    print("-" * 20)
#    print("Введите номер акции которую хотите продать")
#    num = int(input())
#    print("Введите количество акций которые вы хотите продать")
#    count = int(input())
#    if (num < 0 or num > 12):
#        print("Таких акций нет")
#        print("Вы хотите выйти? 1 - Да, 2 - нет")
#        ch = int(input())
#    print(user_stocks[num - 1])
#    if (count <= int(user_stocks[num - 1][3])):
#        user_stocks[num - 1][3] = " " + str(int(user_stocks[num - 1][3]) - count)
#        money += int(user_stocks[num - 1][1]) * count
#        print(f"Вы успешно продали {count} штук акций", "".join(user_stocks[num - 1][0]))
#    else:
#        print("Столько акций нет")


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
