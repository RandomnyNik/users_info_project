import sqlite3
import secret

con = sqlite3.connect(secret.DB_PATH, check_same_thread=False)
cur = con.cursor()

def init():
    with open("./sql/create_table_users_info.sql", 'r') as f:
        cur.execute(f.read())
        con.commit()
    with open("./sql/create_table_questions.sql", 'r') as f:
        cur.execute(f.read())
        con.commit()

def users_load() -> dict:
    a = cur.execute('SELECT * FROM users_info')
    f = a.fetchall()
    users = {}
    for i in f:
        users[i[3]] = {
            "count_of_messages": i[0], 
            "count_of_questions": i[1], 
            "count_of_answers": i[2], 
            "level": i[4],
            "id": i[5]

        }
    return users

def save(id, data):
    data["user_id"] = id
    cur.execute("INSERT INTO users_info ('user_id',             \
                                        'count_of_messages',    \
                                        'count_of_questions',   \
                                        'count_of_answers')     \
                VALUES ({}, {}, {}, {})".format(id,
                                        data['count_of_messages'], 
                                        data['count_of_questions'],
                                        data['count_of_answers']))               
    con.commit()


def ms(user, uid):
    cur.execute('''UPDATE users_info SET count_of_messages = {} WHERE user_id = {}'''.format(
        user["count_of_messages"], str(uid)))
    con.commit()

def level_save(user, uid):
    cur.execute(f"UPDATE users_info SET level = '{user['level']}' WHERE user_id = '{uid}'")
    con.commit()

def que_save_to_user(user, uid):
    cur.execute(f"UPDATE users_info SET id_question = '{user['id_question']}' WHERE user_id = '{uid}'")
    con.commit()

def que_save(question):
    cur.execute(f"INSERT INTO questions ('question') VALUES ('{question}')")            
    con.commit()

def que_find(question):
    return cur.execute(f"SELECT answer FROM questions WHERE question = '{question}'").fetchall()

def que_find_some():
    return cur.execute(f"SELECT id, question FROM questions WHERE answer is null").fetchall()

def answer_save(q_id, answer):
    cur.execute(f"UPDATE questions SET answer = '{answer}' WHERE id = '{q_id}'")
    con.commit()

def get_current_que_id(uid):
    return cur.execute(f"SELECT id_question FROM users_info WHERE user_id = '{uid}'").fetchone()
def que(user, uid):
    cur.execute('''UPDATE users_info SET count_of_questions = {} WHERE user_id = {}'''.format(
        user["count_of_questions"], str(uid)))
    con.commit()
def ans(user, uid):
    cur.execute('''UPDATE users_info SET count_of_answers = {} WHERE user_id = {}'''.format(
        user["count_of_answers"], str(uid)))
    con.commit()

    