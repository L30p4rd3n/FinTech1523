import sqlite3

con = sqlite3.connect("../instance/hella_db.sqlite")
cur = con.cursor()
take = cur.execute(f"SELECT * FROM stocks")
data = take.fetchall()
print(data)
con.close()


# yup
