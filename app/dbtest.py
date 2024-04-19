import sqlite3

con = sqlite3.connect("../instance/hella_db.sqlite")
cur = con.cursor()
uid = input()
sid = input()
take = cur.execute(f"select * FROM Stocks")
take.fetchall()
print(type(take))
a = take.fetchall()
print(take.fetchall())

con.close()


# yup
