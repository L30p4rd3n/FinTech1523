import logging
import random
import sqlite3
import time
from app.poker import play
import flask
from flask import render_template, request, redirect, url_for, flash, Blueprint, abort
from app import db, User, Advise, Stocks, SU, UG, UGS, Gstock
from flask_login import login_required, current_user, logout_user, login_user
from sqlalchemy import and_
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

game = Blueprint("game", __name__, url_prefix="/game")

#f_news = open('news_of_the_day.txt')
#f_stocks = open('stocks.txt')
#news_of_the_day = []
#stocks = []
#user_stocks = []
#for line in f_news:
#    news_of_the_day.append(line)
#
#for line in f_stocks:
#    stocks.append(list(line.split("|")))
#    a = list(line.split("|"))
#    a.append(" 0")
#    user_stocks.append(a)


@game.route('/test')
def load_vari():
    return render_template("send.html")

@game.route('/test', methods=["get", "post"])
def vari():
    user = UG.query.filter_by(uid=current_user.id)
    zeal, foresight, risky = user.zeal, user.foresight, user.risk
    money, tax, salary = user.money, user.tax, user.salary

    #print("Как насчет поработать еще пару часиков? За целых 1,5 зарплаты? Введи 1!")
    #print("Посмотреть свои акции? Введи 2!")
    #print("Инвестировать? Введи 3!")
    #print("Продашь акции? Введи 4!")
    #print("Сыграем? Введи 5!")

    # должно быть в меню, которое видно на ВСЕХ устройствах

    v = request.get_data()
    if (v == 1):
        zeal += 1
        skip()
    elif (v == 2):
        check_stock()
        vari()
    elif (v == 3):
        foresight += 1
        buy()
    elif (v == 4):
        sell()
    elif (v == 5):
        risky += 1
        print("Давай сыграем в покер")
        print("Сколько хочешь поставить?")
        stavka = int(input())
        if (play()):
            money += stavka
        else:
            money -= stavka
    else:
        print("Ну и лан")
    return v


def new_Day():
    user = UG.query.filter_by(uid=current_user.id)
    day, money, salary = user.day, user.money, user.salary
    money += salary
    day += 1
    #stock_change()
    db.session.commit()
    #print(f"Сегодня {day} день, а у вас на счёте {money} рублей")
    # print(news_of_the_day[day - 1]) # TODO news_of_the_day сделать через взятие акций за день в stock_change() и фронт
    return {
        "day": day,
        "money": money
    }

@game.route('/skip', methods=["post"])
def skip():
    user = UG.query.filter_by(uid=current_user.id)
    day, money, salary = user.day, user.money,  user.salary
    money += salary * 1.5
    db.session.commit()
    if (random.random() > 0.7 and day > 10):
        salary *= 1.5
        return {"success": 1,
                "salary": salary}
    return {"success": 0,
            "salary": salary}



@game.route('/check')
def check_stock():
    user_stocks = UGS.query.filter_by(uid=current_user.id)
    if user_stocks != []:
        send = {}
        for i in range(len(user_stocks)):
            send[i] = user_stocks[i]
        return send

    return {0: "У вас нет купленных лотов."} # JSON for equal-type return.


def buy():
    stocks = Gstock.query.all()
    user = UGS.query.filter_by(uid=current_user.id)
    money = user.money
    user_stocks = UGS.query.filter_by(uid=current_user.id)

    # print("Список акций:")
    number = 1
    # for i in stocks: # STOP PUTTING for i in SOMETHING!!! PLS USE for i in range(len(SOMETHING)) D;
        print(number, "|".join(i))
    print("-" * 20)
    print("Введите номер акции которую хотите приобрести")
    num = int(input())
    print("Введите количество акций которые вы хотите приобритсти")
    count = int(input())
    if (num < 0 or num > 12):
        print("Таких акций нет")
        print("Вы хотите выйти? 1 - Да, 2 - нет")
        ch = int(input())
        if ch == 1:
            return 0
    if (count * int(stocks[num - 1][1]) < money):
        user_stocks[num - 1][3] = " " + str(int(user_stocks[num - 1][3]) + count)
        print(f"Вы успешно купили {count} лотов акций", "".join(user_stocks[num - 1][0]))
    else:
        print("Недостаточно денег.")


def stock_change():
    for i in user_stocks:
        if (int(i[3]) > 0):
            pr = int(list(i[2].split("%"))[0])
            pr = 1.1 - pr / 100
            if (random.random() < pr):
                i[1] = str(int(i[1]) + int(i[1]) * int(list(i[2].split("%"))[0]) // 100)


def sell():
    global money
    number = 1
    for i in user_stocks:
        print(number, " | ", "|".join(i))
    print("-" * 20)
    print("Введите номер акции которую хотите продать")
    num = int(input())
    print("Введите количество акций которые вы хотите продать")
    count = int(input())
    if (num < 0 or num > 12):
        print("Таких акций нет")
        print("Вы хотите выйти? 1 - Да, 2 - нет")
        ch = int(input())
    print(user_stocks[num - 1])
    if (count <= int(user_stocks[num - 1][3])):
        user_stocks[num - 1][3] = " " + str(int(user_stocks[num - 1][3]) - count)
        money += int(user_stocks[num - 1][1]) * count
        print(f"Вы успешно продали {count} штук акций", "".join(user_stocks[num - 1][0]))
    else:
        print("Столько акций нет")


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
