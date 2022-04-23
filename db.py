import sqlite3
import secret

con = sqlite3.connect(secret.DB_PATH, check_same_thread=False)
cur = con.cursor()

def init():
    with open("./sql/create_table_users_info.sql", 'r') as f:
        cur.execute(f.read())
        con.commit()

def users_load() -> dict:
    a = cur.execute('SELECT * FROM users_info')
    f = a.fetchall()
    users = {}
    for i in f:
        users[i[3]] = {
            "count_of_messages": i[0], "count_of_questions": i[1], "count_of_answers": i[2], "id": i[4]
        }
    return users

def save(id, data):
    data["user_id"] = id
    cur.execute("INSERT INTO users_info ('user_id',             \
                                        'count_of_messages',    \
                                        'counnt_of_questions',   \
                                        'count_of_answers')     \
                VALUES ({}, {}, {}, {})".format(id,
                                        data['count_of_messages'], 
                                        data['count_of_questions'],
                                        data['count_of_answers']))               
    con.commit()

def ms(b):
    cur.execute('''UPDATE users_info SET count_of_messages = {} WHERE id = 2'''.format(b))
    con.commit()