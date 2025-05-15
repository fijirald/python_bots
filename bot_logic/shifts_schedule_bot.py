# import threading
# import schedule
# import time
# import json
# from types import SimpleNamespace
import telebot
import locale
import sys
import utils
from datetime import datetime, timedelta

os = sys.argv[1]

locale.setlocale(locale.LC_TIME, utils.get_config("locale." + os))
bot = telebot.TeleBot(utils.get_secret("bot_token"))

# button_this_week = telebot.types.InlineKeyboardButton('Смены на этой неделе', callback_data='shift_for_current_week')
# button_next_week = telebot.types.InlineKeyboardButton('Смены на следующей неделе', callback_data='shift_for_next_week')
button_this_week = telebot.types.InlineKeyboardButton('Смены на этой неделе', callback_data='shift_for_current_week')
button_next_week = telebot.types.InlineKeyboardButton('Смены на следующей неделе', callback_data='shift_for_next_week')

keyboard = telebot.types.ReplyKeyboardMarkup()
keyboard.add(button_this_week)
keyboard.add(button_next_week)


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
        utils.shift_for_current_week(bot, call.message.chat.id)
    elif call.data == "shift_for_next_week":
        utils.shift_for_next_week(bot, call.message.chat.id)


@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, f"""/shift_today
/shift_for_date dd.mm.yy
/shift_for_current_week
/shift_for_next_week""")


@bot.message_handler(commands=["shift_today"])
def send_text(message):
    bot.send_message(message.chat.id, utils.get_shift_status_for(datetime.today(), utils.zeroDayTimeShift))


@bot.message_handler(commands=["shift_for_date"])
def send_text(message):
    message_text = message.text.split()[1]
    seeked_date = datetime.strptime(message_text, '%d.%m.%y')
    bot.send_message(message.chat.id, utils.get_shift_status_for(seeked_date, utils.zeroDayTimeShift))


@bot.message_handler(commands=["shift_for_current_week"])
def send_text(message):
    utils.shift_for_current_week(bot, message.chat.id)


@bot.message_handler(commands=["shift_for_next_week"])
def send_text(message):
    utils.shift_for_next_week(message.chat.id)


@bot.message_handler(content_types=["text"])
def send_text(message):
    print(message)
    if (message.text == "Смены на этой неделе"):
        utils.shift_for_current_week(bot, message.chat.id)
    if (message.text == "Смены на следующей неделе"):
        utils.shift_for_next_week(bot, message.chat.id)


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

