import sqlite3
import telebot
import secret

bot = telebot.TeleBot(secret.token_n1)

con = sqlite3.connect('que_answers.db', check_same_thread=False)
cur = con.cursor()
a = cur.execute('SELECT * FROM questions_ans')
f = a.fetchall()
print(f)

qs_as = {}
for i in f:
    qs_as[i[0]] = {
        "answers": i[1], "response_rating": i[2], "id": i[3]
    }


@bot.message_handler(content_types=['text'])
def answer(msg):

    print('Полученно сообщение от пользователя: ', msg.from_user.id, msg.text)
    text = msg.text

    lvl = 0

    if text == "я хочу задать вопрос":
        bot.send_message(msg.from_user.id, "Задавай свой вопрос")

        if text != "я хочу задать вопрос":
            if text in qs_as[id]["questions"]:
                if qs_as[id]["answers"] != "":
                    bot.send_message(msg.from_user.id, qs_as[id]['answers'])

                elif qs_as[id]["answers"] == "":
                    bot.send_message(msg.from_user.id, "Ответов пока нет")

            elif text not in qs_as[id]["questions"]:
                def save_que(a):
                    cur.execute("INSERT INTO questions_ans ('questions') VALUES ('{}')".format(a))
                    con.commit()
                save_que(text)
                bot.send_message(msg.from_user.id, 'Ответов пока нет')

bot.polling(none_stop=True)


