import os
import configparser
from datetime import datetime, timedelta

zeroDayTimeShift = datetime.strptime('10.11.23', '%d.%m.%y')

def get_secret(parameter):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(BASE_DIR, 'config', 'secrets.ini')
    # Загружаем конфигурацию
    config = configparser.ConfigParser()
    config.read(config_path)
    # Получаем словарь параметров
    properties = dict(config['DEFAULT'])
    return properties[parameter]

def get_config(parameter):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(BASE_DIR, 'config', 'app.ini')
    # Загружаем конфигурацию
    config = configparser.ConfigParser()
    config.read(config_path)
    # Получаем словарь параметров
    properties = dict(config['DEFAULT'])
    return properties[parameter]



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
    return None
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


def shift_for_current_week(bot, chat_id):
    now = datetime.now()
    monday = now - timedelta(days=now.weekday())
    result = get_shifts_for_week(monday)
    bot.send_message(chat_id, result, "markdown")

def shift_for_next_week(bot, chat_id):
    now = datetime.now()
    monday = now - timedelta(days=now.weekday()) + timedelta(days=7)
    result = get_shifts_for_week(monday)
    bot.send_message(chat_id, result, "markdown")