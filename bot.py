import telebot
import os


class User:
    def __init__(self, name, user_id):
        self.name = name
        self.id = user_id


class Calculator:
    def __init__(self, msg = ' '):
        self.msg = msg


TOKEN = os.environ['TOKEN']
bot = telebot.TeleBot(TOKEN)


def init_user(message):
    user = User(message.text, message.from_user.id)
    bot.send_message(message.chat.id, f'Hello: {user.name}, your id: {user.id}')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Напишіть дію у вигляді: 11:30+1.30 або 15:15+0.45')
    bot.register_next_step_handler(message, calculate)


def calculate(message):
    calc = Calculator(msg = message.text)
    try:
        row = str(calc.msg).replace(' ', '').split('+')
        time_1 = row[0]
        time_2 = row[1]
        if str(time_1)[2] != ':' and len(str(time_1)) != 5:
            bot.send_message(message.chat.id, 'Неправильний формат введіть /start щоб спробувати знову!')
        time_1 = str(time_1).strip().split(':')
        if str(time_2)[1] != '.' and len(str(time_2)) != 4:
            bot.send_message(message.chat.id, 'Неправильний формат введіть /start щоб спробувати знову!')
        time_2 = str(time_2).strip().split('.')
        if time_1[1] == '00':
            time_1[1] = '0'
        if time_2[1] == '00':
            time_2[1] = '0'
        hours = int(time_1[0]) + int(time_2[0])
        mins = int(time_1[1]) + int(time_2[1])
        if mins >= 60:
            hours = hours + 1
            mins = mins - 60
        if mins == 0:
            mins = '00'
        if len(str(mins)) == 1:
            mins = '0' + str(mins)

        bot.send_message(message.chat.id, f"Відповідь: {hours}:{mins}")

    except Exception as e:
        bot.send_message(message.chat.id, 'Неправильний формат введіть /start щоб спробувати знову!')


@bot.callback_query_handler(func=lambda call: True)
def handle(call):
    if call.data == 'info':
        bot.send_message(call.message.chat.id, 'Data: {}'.format(str(call.data)))
        bot.answer_callback_query(call.id)
    elif call.data == 'download':
        bot.send_message(call.message.chat.id, f'Send the photo (user id: {call.message.from_user.id})')
    elif call.data == 'params':
        bot.send_message(call.message.chat.id, 'Data: {}'.format(str(call.data)))
        bot.answer_callback_query(call.id)
    else:
        bot.send_message(call.message.chat.id, 'Try to retry!')
        bot.answer_callback_query(call.id)

'''
@bot.message_handler(content_types=['text'])
def text_msg(message):
    if str(message.text).lower() == 'send to lera':
        msg = bot.send_message(message.chat.id, 'Enter the message')
        bot.register_next_step_handler(msg, send_lera)
    else:
        next

def send_lera(message):
    bot.send_message(lera_id, message.text)
'''


@bot.message_handler(content_types=['photo'])
def photo_msg(message):
    bot.send_message(message.chat.id, 'Photo was downloaded!')


@bot.message_handler(content_types=['document'])
def file_msg(message):
    bot.send_message(message.chat.id, 'Document was downloaded!')





bot.polling()