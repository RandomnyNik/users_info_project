import telebot
from telebot import types
import secret
import db
import analyze
import random

bot = telebot.TeleBot(secret.TOKEN)
db.init()
print(db.cur)

users = db.users_load()
print(users)
users_analyze = {}

markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
markup.add(types.KeyboardButton("Задать вопрос"), types.KeyboardButton("Дать ответ"))

"""
Описывает работу бота
"""
@bot.message_handler(content_types=['text'])
def answer(msg):
    print('Полученно сообщение от пользователя: ', msg.from_user.id, msg.text)
    text = msg.text.lower()

    if msg.from_user.id in users:
        if not users[msg.from_user.id]["level"]:
            users[msg.from_user.id]["level"] = "menu"
            db.level_save(users[msg.from_user.id], msg.from_user.id)
        response = ""
        if (users[msg.from_user.id]["level"] == "menu"):
            response = menu_handler(msg)
        elif (users[msg.from_user.id]["level"] == "question"):
            response = que_handler(msg)
        elif (users[msg.from_user.id]["level"] == "answer"):
            response = answer_handler(msg)
        if response == "break":
            return
    else:
        create_user(msg)

    bot.send_message(msg.from_user.id, "Задай вопрос", reply_markup=markup)


def create_user(msg):
    users[msg.from_user.id] = {
        "count_of_messages": 1,
        "count_of_questions": 0,
        "count_of_answers": 0,
        "level": "menu"
    }
    # Создаем аналатику пользователя
    users_analyze[msg.from_user.id] = analyze.new_user()
    db.save(msg.from_user.id, users[msg.from_user.id] )
    bot.send_message(msg.from_user.id, " Я тебя не знаю")

def que_handler(msg):
    question = msg.text.lower()
    answer = db.que_find(question)
    if answer:
        answer = answer[0]
    if not answer:
        db.que_save(question)
        bot.send_message(msg.from_user.id, 'не нашел ответа')
    else:
        bot.send_message(msg.from_user.id, answer)
    users[msg.from_user.id]["level"] = "menu"
    db.level_save(users[msg.from_user.id], msg.from_user.id)

    return "continue"

def answer_handler(msg):
    #q_id = users[msg.from_user.id]["id_question"]
    q_id = db.get_current_que_id(msg.from_user.id)[0]
    db.answer_save(q_id, msg.text)
    users[msg.from_user.id]["level"] = "menu"
    db.level_save(users[msg.from_user.id],msg.from_user.id )

    return "continue"


def menu_handler(msg):
    #### Count
    print(users[msg.from_user.id])
    count_ms = users[msg.from_user.id]["count_of_messages"] + 1
    users[msg.from_user.id]["count_of_messages"] =  count_ms
    bot.send_message(msg.from_user.id, 'Ты писал мне  {}  раз'.format(
            count_ms
    ))
    db.ms(users[msg.from_user.id], msg.from_user.id)

    #### Analyze
    if msg.from_user.id in users_analyze:
        analyze.handler(users_analyze[msg.from_user.id], msg.text)
        print(users_analyze[msg.from_user.id])
    else:
        users_analyze[msg.from_user.id] = analyze.new_user()
    
    #### Body

    if msg.text.lower() == "задать вопрос":
        users[msg.from_user.id]["level"] = "question"
        db.level_save(users[msg.from_user.id],msg.from_user.id )
        bot.send_message(msg.from_user.id, "Давай задавай", reply_markup = types.ReplyKeyboardRemove())
        return "break"
    elif msg.text.lower() == "дать ответ":
        questions = db.que_find_some()
        print(questions)
        if not questions:
            bot.send_message(msg.from_user.id, f"Вопросов нет")
        else:
            que = random.choice(questions)
            bot.send_message(msg.from_user.id, f"Ответь {que[1]}")
            users[msg.from_user.id]["level"] = "answer"
            users[msg.from_user.id]["id_question"] = que[0]
            db.que_save_to_user(users[msg.from_user.id],msg.from_user.id)
            db.level_save(users[msg.from_user.id],msg.from_user.id )
        return "break"

bot.polling(non_stop=True)