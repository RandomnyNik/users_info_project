import telebot
import secret
import db

bot = telebot.TeleBot(secret.TOKEN)
db.init()
print(db.cur)

users = db.users_load()
print(users)

"""
Описывает работу бота
"""
@bot.message_handler(content_types=['text'])
def answer(msg):
    print('Полученно сообщение от пользователя: ', msg.from_user.id, msg.text)
    #count_ms = users[msg.from_user.id]["count_of_messages"]
    text = msg.text.lower

    if msg.from_user.id in users:
        count_ms = users[msg.from_user.id]["count_of_messages"]
        users[msg.from_user.id]["count_of_messages"] = count_ms + 1
        bot.send_message(msg.from_user.id, 'Ты писал мне ' + str(count_ms) + " раз")
        db.ms(count_ms)
    else:
        users[msg.from_user.id] = {
            "count_of_messages": 1,
            "count_of_questions": 0,
            "count_of_answers": 0
        }
        db.save(msg.from_user.id, users[msg.from_user.id] )
        bot.send_message(msg.from_user.id, " Я тебя не знаю")

bot.polling(non_stop=True)