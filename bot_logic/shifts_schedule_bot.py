# import threading
# import schedule
# import time
# import json
# from types import SimpleNamespace
import telebot
import locale
import sys
from datetime import datetime, timedelta
from jproperties import Properties

secrets = Properties()
configs = Properties()

with open('../config/secrets.properties', 'rb') as config_file:
    secrets.load(config_file)

with open('../config/app.properties', 'rb') as config_file:
    configs.load(config_file)


os = sys.argv[1]

locale.setlocale(locale.LC_TIME, configs.get("locale." + os).data)

bot = telebot.TeleBot(secrets.get("bot_token").data)

# button_this_week = telebot.types.InlineKeyboardButton('Смены на этой неделе', callback_data='shift_for_current_week')
# button_next_week = telebot.types.InlineKeyboardButton('Смены на следующей неделе', callback_data='shift_for_next_week')
button_this_week = telebot.types.InlineKeyboardButton('Смены на этой неделе', callback_data='shift_for_current_week')
button_next_week = telebot.types.InlineKeyboardButton('Смены на следующей неделе', callback_data='shift_for_next_week')

keyboard = telebot.types.ReplyKeyboardMarkup()
keyboard.add(button_this_week)
keyboard.add(button_next_week)

zeroDayTimeShift = datetime.strptime('10.11.23', '%d.%m.%y')


def get_shift_status_for(seeked_day, zero_day_time_shift):
    diff_time = seeked_day - zero_day_time_shift
    if diff_time.days % 4 == 1:
        return "В ночь"
    elif diff_time.days % 4 == 2:
        return "С ночи/Отсыпной"
    elif diff_time.days % 4 == 3:
            return "Выходной"
    elif diff_time.days % 4 == 0:
        return "В день"
    # match diff_time.days % 4:
    #     case 1:
    #         return "В ночь (Night shift)"
    #     case 2:
    #         return "С ночи/Отсыпной (After-night-shift day / Sleeping day)"
    #     case 3:
    #         return "Выходной (Full non-working day)"
    #     case _:
    #         return "В день (Day shift)"


def get_shifts_for_week(monday):
    result = ""
    for x in range(0, 7):
        day_x = monday + timedelta(days=x)
        shift_status = get_shift_status_for(day_x, zeroDayTimeShift)
        bold = ""
        if day_x.date() == datetime.today().date():
            bold = "*"
        result += f"{bold}" \
                  f"{day_x.strftime('%a')} ({day_x.strftime('%d %b')}) - {shift_status} " \
                  f"{'(сегодня)' if day_x.date() == datetime.today().date() else ''}" \
                  f"{bold}"
        if x < 7:
            result += "\n"
    return result


@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(message.chat.id, text="Нажмите на нужную кнопку внизу:", reply_markup=keyboard)
#     bot.reply_to(message, """/shift_today
# /shift_for_date dd.mm.yy
# /shift_for_current_week
# /shift_for_next_week""")


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "shift_for_current_week":
        shift_for_current_week(call.message.chat.id)
    elif call.data == "shift_for_next_week":
        shift_for_next_week(call.message.chat.id)


@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, f"""/shift_today
/shift_for_date dd.mm.yy
/shift_for_current_week
/shift_for_next_week""")


@bot.message_handler(commands=["shift_today"])
def send_text(message):
    bot.send_message(message.chat.id, get_shift_status_for(datetime.today(), zeroDayTimeShift))


@bot.message_handler(commands=["shift_for_date"])
def send_text(message):
    message_text = message.text.split()[1]
    seeked_date = datetime.strptime(message_text, '%d.%m.%y')
    bot.send_message(message.chat.id, get_shift_status_for(seeked_date, zeroDayTimeShift))


@bot.message_handler(commands=["shift_for_current_week"])
def send_text(message):
    shift_for_current_week(message.chat.id)


def shift_for_current_week(chat_id):
    now = datetime.now()
    monday = now - timedelta(days=now.weekday())
    result = get_shifts_for_week(monday)
    bot.send_message(chat_id, result, "markdown")


@bot.message_handler(commands=["shift_for_next_week"])
def send_text(message):
    shift_for_next_week(message.chat.id)


def shift_for_next_week(chat_id):
    now = datetime.now()
    monday = now - timedelta(days=now.weekday()) + timedelta(days=7)
    result = get_shifts_for_week(monday)
    bot.send_message(chat_id, result, "markdown")


@bot.message_handler(content_types=["text"])
def send_text(message):
    print(message)
    if (message.text == "Смены на этой неделе"):
        shift_for_current_week(message.chat.id)
    if (message.text == "Смены на следующей неделе"):
        shift_for_next_week(message.chat.id)


print(f"{datetime.today().strftime('%d.%m.%Y %H:%M:%S')} starting...")

bot.polling(none_stop=True)

# chatId = 0

# @bot.message_handler(content_types=["text"])
# def send_text(message):
#     bot.send_message(message.chat.id, message.text)


# @bot.message_handler(commands=["cron_stop"])
# def send_text(message):
#     print("cron stopped...")
#     global chatId
#     chatId = 0


# @bot.message_handler(commands=["cron_start"])
# def send_text(message):
#     global chatId
#     if chatId == 0:
#         print("cron started...")
#         chatId = message.chat.id
#         while chatId != 0:
#             bot.send_message(chatId, "I'm working...")
#             time.sleep(5)

