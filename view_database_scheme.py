import sqlite3

con = sqlite3.connect("part_db/Users_info_project.db", check_same_thread=False)
cur = con.cursor()

cur.execute("SELECT * FROM sqlite_master")

data = cur.fetchall()
for i in data:
    print(i)

