from app import app, db, User, Advise, Stocks, Gstock
from datetime import date, timedelta
import sqlite3


def creator():
    with app.app_context():
        #db.drop_all()
        db.create_all()
    return "success in creating"
creator()


# for i in range(1, 3):
#    with app.app_context():
#        s = Stocks(id=i, cdate="06-02-2023", boardid=f'TST{i}', oneprice=i*69)
#        db.session.add(s)
#        db.session.commit()
# a = Advise(id=0, adv_type=4, adv=advices[0])
# db.session.add(a)
# db.session.commit()
def create_stocks():
    f = open("app/codes.txt")
    x = open("app/names.txt", encoding="utf-8")
    a = f.readline().replace('\n', '')
    b = x.readline().replace('\n', '')
    i = 1
    while a:
        a = f.readline().replace('\n', '')
        b = x.readline().replace('\n', '')
        with app.app_context():
            ydate = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
            s = Stocks(id=i, fname=str(b), ydate=ydate, boardid=str(a), dm1price=0, dm2price=0, dm3price=0, dm4price=0,
                       dm5price=0, dm6price=0, dm7price=0)
            db.session.add(s)
            db.session.commit()
        i += 1
    print(f"created {i} stocks templates")
    return 0

#create_stocks()

def cgs():

    f = open("app/gnames.txt", encoding="utf-8")
    a = f.readline().replace('\n', '')
    while a:
        a = f.readline().replace('\n', '')
        b = a.split("|")
        print(b)
        for i in range(1, 32):
            with app.app_context():
                if(b[-2] == "Рисковая"):
                    s = Gstock(bid=int(b[0]),name=b[1], bcode=b[2], date=i, price=0.000, risk=1)
                else:
                    s = Gstock(bid=int(b[0]), name=b[1], bcode=b[2], date=i, price=0.000, risk=0)
                db.session.add(s)
                db.session.commit()
def change_name():
    with app.app_context():
        need = Gstock.query.filter_by(name='Биржа "Деньги Лопатами"').all()
        for i in range(len(need)):
            need[i].name = 'Биржа "Качество, а не Время"'
        db.session.commit()
#change_name()

def create_adv():
    f = open("app/advices.txt", encoding="utf-8")
    a = f.readline().replace('\n', '')
    i = 0
    while a:
        a = f.readline().replace('\n', '')
        with app.app_context():
            adv = Advise(adv = a, type = i % 5 + 1)
            db.session.add(adv)
            db.session.commit()
        i += 1
    print(f"created {i} advs")
    return 0
#create_adv()