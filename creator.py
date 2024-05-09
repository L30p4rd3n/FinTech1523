from app import app, db, User, Advise, Stocks, AU, Gstock
from datetime import date, timedelta


def creator():
    with app.app_context():
        #db.drop_all()
        db.create_all()
    return "success in creating"
creator()


advices = [
    "Автоматизируйте сбережения: Настройте автоматические переводы средств на сберегательный счет или инвестиционный счет ежемесячно. Это поможет создать привычку к регулярному сбережению.",

    "Составьте бюджет: Оцените свои ежемесячные доходы и расходы. Это поможет определить, где можно сократить расходы и высвободить средства для сбережений.",

    "Создайте цели: Установите конкретные цели сбережений на короткий и долгий срок. Это поможет вам лучше фокусироваться на сохранении денег.",

    "Разнообразификация портфеля: Распределите свои инвестиции между различными активами, такими как акции, облигации, недвижимость и т. д. Это поможет снизить общий уровень риска в случае падения цен на какой-то один тип активов.",

    "Инвестируйте в фонды с риском, подходящим вашему профилю: Если вы хотите вкладывать в акции, рассмотрите инвестирование через взвешенные портфели ETF или инвестиционные фонды, которые предлагают диверсификацию и уменьшают риск.",

    "Изучите рынок: Хорошее знание того, куда вы инвестируете, может снизить ваш риск. Исследуйте компании и секторы, в которые вы планируете инвестировать, и следите за новостями и тенденциями.",

    "Образование и исследования: Изучите основы инвестирования в акции, разберитесь с ключевыми показателями и методами анализа, чтобы принимать более обоснованные решения.",

    "Долгосрочная перспектива: Инвестиции в акции часто более успешны на долгосрочном горизонте. Будьте готовы держать активы на протяжении длительного времени.",

    "Диверсификация портфеля: Не вкладывайте все средства в одну акцию или один сектор. Разнообразие помогает снизить риски.",

    "Сбережения и аварийный фонд: Откладывайте средства на сберегательный счет для неожиданных расходов. Это позволит вам чувствовать себя более защищенно в случае финансовых кризисов или неожиданных обстоятельств.",

    "Инвестиции с низким риском: Рассмотрите вложения в более консервативные инструменты, такие как облигации или облигации с фиксированным доходом, которые обычно менее подвержены рыночным колебаниям.",

    "Фонды рынка денежных средств: Это инвестиционные продукты, обычно имеющие низкий риск и высокую ликвидность. Они могут быть более стабильными в сравнении с акциями."
] # cringe


def add_data(advice: list):
    k = 0
    for i in range(1, 5):
        for j in range(3):
            with app.app_context():
                a = Advise(adv_type=i, adv=advice[k])
                db.session.add(a)
                db.session.commit()
            k += 1
    print(f"created {k} advices")


#creator()
#add_data(advices)


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