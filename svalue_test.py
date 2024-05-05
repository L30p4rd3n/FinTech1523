import random
import matplotlib.pyplot as plt
from app import db, Gstock, app

c = [[], [], [], [], [], [], [], [], [], []]
__s__ = [34.000, 0.943, 13.543, 130.000, 7.130, 63.000, 26.429, 46.000, 9.100, 13.730]

for j in range(10):
    s = __s__[j]
    for i in range(31):
        if i < 7:
            s += float(format((int(random.random() // 0.001 % 1000) / 1000), '.3f'))
        elif i == 7:
            s -= float(format((int(random.random() // 0.001 % 1000) / 1000) * random.randint(1, 5), '.3f'))
        elif i > 7 and i < 13:
            s += float(format((int(random.random() // 0.001 % 1000) / 1000), '.3f'))
        elif i == 13:
            s += float(format((int(random.random() // 0.001 % 1000) / 1000) * 1.4, '.3f'))
        elif i > 13 and i < 18:
            s -= float(format((int(random.random() // 0.001 % 1000) / 1000), '.3f'))
        elif i >= 18 and i < 19:
            s -= float(format((int(random.random() // 0.001 % 1000) / 1000), '.3f'))
        elif i >= 19 and i < 27:
            s += float(format((int(random.random() // 0.001 % 1000) / 1000) * 0.569, '.3f'))
        elif i >= 27 and i < 30:
            s -= float(format((int(random.random() // 0.001 % 1000) / 1000), '.3f'))
        else:
            s += float(format((int(random.random() // 0.001 % 1000) / 1000), '.3f'))
        c[j].append(s)
# TODO - коэффициент и работа с ним, надо как-то разнообразить это всё.
for i in range(10):
    for j in range(31):
        c[i][j] = float(format(c[i][j], ".3f"))
for i in range(10):
    print(c[i])

def add_stable(bid):
    with app.app_context():
        a = Gstock.query.filter_by(bid=bid).all()
        for i in range(31):
            a[i].price = c[bid - 1][i]
        db.session.commit()
add_stable(2)
add_stable(5)
add_stable(7)
add_stable(9)
add_stable(10)

for i in range(10):
    plt.plot(c[i])

plt.show()