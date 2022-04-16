import sqlite3
import telebot
import secret

bot = telebot.TeleBot(secret.token_n1)

con = sqlite3.connect('Users_info_project.db', check_same_thread=False)
cur = con.cursor()
a = cur.execute('SELECT * FROM users_info')
f = a.fetchall()
print(f)

users = {}
for i in f:
    users[i[3]] = {
        "count_of_messages": i[0], "count_of_questions": i[1], "count_of_answers": i[2], "id": i[4]
    }

def save(a):
    cur.execute("INSERT INTO users_info ('user_id') VALUES ('{}')".format(a))
    con.commit()

def ms(b):
    cur.execute('''UPDATE users_info SET count_of_messages = {} WHERE id = 2'''.format(b))
    con.commit()

print(users)
@bot.message_handler(content_types=['text'])
def answer(msg):

    print('Полученно сообщение от пользователя: ', msg.from_user.id, msg.text)

    count_ms = users[msg.from_user.id]["count_of_messages"]
    ms(count_ms)

    text = msg.text.lower

    if msg.from_user.id in users:
        users[msg.from_user.id]["count_of_messages"] += 1
        bot.send_message(msg.from_user.id, 'Ты писал мне ' + str(users[msg.from_user.id]["count_of_messages"]) + " раз")

    else:
        users[msg.from_user.id]["count_of_messages"] = 1
        save(msg.from_user.id)
        bot.send_message(msg.from_user.id, " Я тебя не знаю")





bot.polling(non_stop=True)