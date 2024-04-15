import sqlite3

con = sqlite3.connect("../instance/hella_db.sqlite")
cur = con.cursor()
uid = input()
sid = input()
take = cur.execute(f"select * FROM su WHERE uid='{uid}' AND sid='{sid}'")
take.fetchall()
delete = cur.execute(f"DELETE FROM su WHERE uid='{uid}' AND sid='{sid}'")
take = cur.execute(f"select * FROM su WHERE uid='{uid}' AND sid='{sid}'")
take.fetchall()

con.close()


# yup
