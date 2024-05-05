import sqlite3




con = sqlite3.connect("../instance/hella_db.sqlite")
cur = con.cursor()
take = cur.execute(f"SELECT * FROM Gstock")
data = take.fetchall()
a = cur.execute(f"SELECT * FROM UGS WHERE gsid={2} AND uid={1}")
print(a.fetchone())
print(data)
con.close()


# yup
