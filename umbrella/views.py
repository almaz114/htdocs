from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection
from .forms import *
import json
# import numpy as np
# from django.contrib.gis.shortcuts import numpy     # эксперимент для numpy
# from django.contrib.gis.shortcuts import numpy
# from django.contrib import numpy        # импорт numpy из папки django
from django.http import JsonResponse
import datetime
import os
from datetime import date, time, timedelta
from datetime import datetime
import time
from find_file import find_file
from loguru import logger
from notifiers import get_notifier             # уведомления telegram
from Postgres_Class import save_zayvka_to_db   # сохранение заявок в бд
import environ

# ==================== GET CONFIG FROM ENVIROMENT =====================
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
# reading .env file
environ.Env.read_env()
string_env = os.environ
logger.info(f"{string_env=}\n")
logger.info(f"\n{string_env['APP_NAMES']=}")
logger.info(f"\n{string_env['BASE_DIR']=}")

# ========= G E T  A P P C O N F I G ========================================================
dict_base_config = json.loads(string_env['APP_NAMES'])
logger.info(f"{dict_base_config=}, {type(dict_base_config)=}")

if string_env['APP_NAMES'] is None:
    logger.error(f"Не найдена переменная окружения: APP_NAMES,  {type(string_env)=}")
elif isinstance(string_env['APP_NAMES'], str):
    configs_dict = json.loads(string_env['APP_NAMES'])
    config_app_name = configs_dict['umbrella']   # имя нашего приложения/папки с конфигами в файле .env

    if 'BASE_DIR' in string_env:
        base_dir_app = string_env['BASE_DIR'] + '\\' + config_app_name + '\\files\\'
        logger.info(f"{base_dir_app=}")
    elif 'BASE_DIR' not in string_env:
        logger.info(f"{string_env['ALTERNATIVE_BASE_DIR']=}, {type(string_env['ALTERNATIVE_BASE_DIR'])=}")
        base_dir_app = string_env['ALTERNATIVE_BASE_DIR'] + '\\' + config_app_name + '\\files\\'
        logger.info(f"{base_dir_app=}")

# ========= G E T  D A T A B A S E  C O N F I G  ===================================================
if string_env['DATABASE'] is None:
    logger.error(f"Не найдена переменная окружения: DATABASE,  {type(string_env)=}")
elif isinstance(string_env['DATABASE'], str):
    postgres_dict = json.loads(string_env['DATABASE'])
    database = postgres_dict['database']
    user = postgres_dict['user_name_db']
    password = postgres_dict['password']
    host = postgres_dict['host']
    port = postgres_dict['port']
    logger.info(f"{postgres_dict=}")


# ========================= Telegram ============================================================
with open(base_dir_app + 'telegram_bot.json', 'r') as file:
    # Чтение файла 'data.json' и преобразование
    # данных JSON в объекты Python
    data = json.load(file)
    token = data["Token"]
    chat_id = data["Chat_id"]
    # logger.info(f"{data=}\n")


# ---  Б А З О В Ы Й  П У Т Ь  К  Ф А Й Л А М  К О Н Ф И Г У Р А Ц И И  J S O N ------------------
# path_config_1 = "C:\\Users\\Almaz\\PycharmProjects\\Django_projects\\htdocs\\files\\"
# path_config_2 = "C:\\Users\\Almaz\\Desktop\\htdocs\\files\\"
# path_config_3 = "C:\\xampp\\htdocs\\almaz\\files\\"
# path_dir = [path_config_1, path_config_2, path_config_3]

if os.path.exists(base_dir_app):
    logger.info(f"Путь с конфигами вашего app сушествует: {base_dir_app=}")
elif not os.path.exists(i):
    logger.error(f"Пути данного не сушествует: {base_dir_app}")


def main(request):
    """ Главная страница проекта Umbrella """
    with open(base_dir_app + 'kovach_signals.json') as f:
        dict_a = json.load(f)

    if request.method == "POST":
        today_time = datetime.today().strftime("%d-%m-%Y-%H:%M")  # получим тек время
        dict_a["last_update"] = str(today_time)  # add date/time to dict

    # ========== Отправка заявки на аренду/покупку продукта на сайте и сохранение её в БД на сервере ===
    if request.POST.get("action") == "ajax_send_zayvka":
        logger.info(f"check alamaz ajax send !!!")

        selected_mentor = request.POST.get('selected_mentor')       # откуда пришли
        name_user = request.POST.get('name_user')                   # имя пользователя
        email = request.POST.get('email_value')
        message_text = request.POST.get('message_text')
        today_time = datetime.today().strftime("%Y-%m-%d %H:%M:%S")    # получим тек время

        dict_new = {"name": "", 'email': "", 'mentor': "", 'message_user': "", 'timeupdate': ""}       # empty dict
        # dict_new = {"name": "regina", 'email': 'hinomura@gmail.com', 'mentor': 'facebook',
        #             'message_user': "buy", 'timeupdate': '2099-01-08 04:05:09'}

        if isinstance(selected_mentor, str) and len(selected_mentor) > 0:
            dict_new['mentor'] = selected_mentor
        if isinstance(name_user, str) and len(name_user) > 0:
            dict_new['name'] = name_user
        if isinstance(email, str) and len(email) > 0:
            dict_new['email'] = email
        if isinstance(message_text, str) and len(message_text) > 0:
            dict_new['message_user'] = message_text
        if isinstance(today_time, str) and len(today_time) > 0:
            dict_new['timeupdate'] = today_time

        logger.info(f"{dict_new=}")
        # SAVE DATA TO DATABASE
        save_zayvka_to_db(database=database, user=user, password=password, host=host, port=port, dict_name=dict_new)

        # new method to db
        # with connection.cursor() as cursor:
        #     cursor.execute(f"insert into zayavki (username, email, mentor, message_user, timeupdate) values ('{name_user}', '{email}', '{selected_mentor}', 'message_text', '{today_time}')")

        # SEND TELEGRAM NOTIFY
        telegram = get_notifier('telegram')
        telegram.notify(message=f'Вам новая заявка от сайта Umbrella: пользователь: {name_user}, {email}, Сообщение: {message_text} !!!', token=token, chat_id=chat_id)

        return HttpResponse(f"ajax test return: {email}, {selected_mentor}, {name_user}, {message_text}")

    else:
        # userform = Test_Form()
        # return render(request, "almaz/write.html", {"form": userform})
        return render(request, "umbrella/umbrella-co.html")


def about(request):
    """ Форма вывода данных ввиде json """
    with open(base_dir_app + 'users_expire_data.json') as f:
        dict_a = json.load(f)
    # data = {"status 1": 1, "status 2": 2}
    # logger.info(f"\ndata: {data}")
    return JsonResponse(dict_a)


def statistics_site(request):
    """
    раздел сайта посвященного статистике работы алгоритмического робота/системы
    """
    labels = []
    data = []

    labels_2 = []
    data_2 = []

    # торгуемые инструменты
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM CURRENCIES")
        row = cursor.fetchall()
        # values = []
        for i, val in enumerate(row):
            # logger.info(f"value row_2: {val}, {val[0]}")
            labels.append(val[1])   # for chart js
            data.append(val[2])     #
            time.sleep(0.4)

    # доходность по месяцам
    with connection.cursor() as cursor_2:
        cursor_2.execute(f"SELECT month, profit_loss FROM profits_month")
        row_2 = cursor_2.fetchall()
        # values = []
        for i, val in enumerate(row_2):
            logger.info(f"value row_2: {val}, {val[0]}")
            labels_2.append(val[0])   # for chart js
            data_2.append(val[1])     #

    return render(request, 'umbrella/statistik.html', {
        'labels': labels,
        'data': data,
        'labels_2': labels_2, 'data_2': data_2})
