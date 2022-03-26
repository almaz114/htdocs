from django.http import HttpResponse
from django.shortcuts import render
from .forms import *

# from class_json import read_from_json  # для работы с json
import json
# import numpy as np
# from django.contrib.gis.shortcuts import numpy     # эксперимент для numpy
# from django.contrib import numpy        # импорт numpy из папки django
from django.http import JsonResponse

import datetime
import os

from datetime import date, time, timedelta
from datetime import datetime

# from find_file import find_file
from loguru import logger

# ---  Б А З О В Ы Й  П У Т Ь  К  Ф А Й Л А М  К О Н Ф И Г У Р А Ц И И  J S O N ------------------
path_config_1 = "C:\\Users\\Almaz\\PycharmProjects\\GUI\\Modern_Gui_MT\\files\\"
path_config_2 = "C:\\Users\\axmetxanov.ikt\\PycharmProjects\\Web_projects\\htdocs_working\\files\\"
path_config_3 = "C:\\xampp\\htdocs\\almaz\\files\\"
path_dir = [path_config_1, path_config_2, path_config_3]
for i in path_dir:
    if os.path.exists(i):
      # logger.info(f"Yes: {i}")
        path_config = i
    elif not os.path.exists(i):
        logger.error(f"No file: {i}")


def index(request):
    """простая функция представления"""
    # with open('files/hedge_martin.json') as f:
    #     d = json.load(f)
    #     print(d)

    return HttpResponse("Страница приложения almaz")


# -- пример № 2 применение шаблонов
def index_2(request):
    """простая функция представления"""
    # dict_a = read_from_json(path_file="files/account_info.json")  # read levels from json file
    # login = dict_a["Login"]  # загружаем значения_список для данного ключа

    data = {"header": "Hello Django", "message": "Welcome to Python"}
    return render(request, "almaz/index.html", context=data)
    # return render(request, "almaz/index.html", {"menu": menu})


# -- пример № 3 применение шаблонов: из раных типов массивов данных (списка, словаря)
def index_3(request):
    """простая функция представления"""
    # dict_a = read_from_json(path_file="files/account_info.json")  # read levels from json file
    # login = dict_a["Login"]  # загружаем значения_список для данного ключа

    header = "Personal Data"  # обычная переменная
    langs = ["English", "German", "Spanish"]  # массив
    user = {"name": "Tom", "age": 23}  # словарь
    addr = ("Абрикосовая", 23, 45)  # кортеж
    data = {"header": header, "langs": langs, "user": user, "address": addr}

    return render(request, "almaz/worker.html", context=data)


# @logger.catch()
def global_levels(request):
    """Метод для редкатирования настроек global_levels в файле json """
    if os.path.exists("C:/xampp/htdocs/almaz/files/global_levels.json"):
        with open("C:/xampp/htdocs/almaz/files/global_levels.json") as f:
            # dict_a = json.load(f)
            # symbols_temp = list(dict_a)  # получаем список всех ключей словаря dict_a, список валют.пар
            # symbols_fx = [key for key in symbols_temp if key != "last_update"]  # исключаем не нужные ключи
            print("файл сушествует")

    else:
        print("файл не сушествует")

    with open("C:/xampp/htdocs/almaz/files/global_levels.json") as f:
        dict_a = json.load(f)
        symbols_temp = list(dict_a)  # получаем список всех ключей словаря dict_a, список валют.пар
        symbols_fx = [key for key in symbols_temp if key != "last_update"]  # исключаем не нужные ключи
        print("файл сушествует")

    if request.method == "POST":
        today_time = datetime.today().strftime("%d-%m-%Y-%H:%M")  # получим тек время
        dict_a["last_update"] = str(today_time)  # add date/time to dict

        # get new data from form on a html
        high_level_new = request.POST.get("high_level")
        print(f"high_level_new: {high_level_new}")

        low_level_new = request.POST.get("low_level")  # получение значения поля age
        sell_stop_price = request.POST.get("sell_stop_price")  # получаем цену соот-го ордера
        buy_stop_price = request.POST.get("buy_stop_price")
        stop_loss_pips = request.POST.get("stop_loss_pips")
        cascade_orders = int(request.POST.get("cascade_orders"))
        close_order = int(request.POST.get("close_order"))

        type_order = int(request.POST.get("type_order"))
        print(f"cascade_orders: {cascade_orders}")

        # пробегаем циклом по всем ключам словаря
        currency = int(request.POST.get("currency"))  # get currency aka "EURUSD"
        print(f"выбрана след валютная пара: {type(currency)}")
        # print(f"всего валютных пар: {symbols_fx}")

        # -- Важно чтобы порядок списка валютных пар в файле json совпадал с порядком на форме html !!!
        for item in enumerate(symbols_fx, start=1):
            print(f"item: {item[0]}")

            if currency == item[0]:
                print(f"выбрана след валютная пара: {currency, item[1]}")
                dict_b = dict_a[item[1]]       # get dict in base_dict for this currency

                print(f"type_order: {type_order}")

                dict_b["high_level"] = float(high_level_new)           # put new_values to dict
                dict_b["low_level"] = float(low_level_new)
                dict_b["stop_loss_pips"] = int(stop_loss_pips)
                dict_b["sell_stop_price"] = float(sell_stop_price)
                dict_b["buy_stop_price"] = float(buy_stop_price)

                # type order methods
                if type_order == 1:
                    # режим лимитных ордеров
                    dict_b["limit_order_type"] = 1
                    dict_b["stop_order_type"] = 0
                else:
                    if type_order == 2:
                        # режим stop ордеров (пробойные ордера)
                        dict_b["limit_order_type"] = 0
                        dict_b["stop_order_type"] = 1

                # cascade method
                if cascade_orders == 0:
                    # cascade false
                    dict_b["cascade_orders"] = 0
                    print("Каскадный режим: отключен")
                else:
                    if cascade_orders == 1:
                        # cascade true
                        dict_b["cascade_orders"] = 1
                        print("Каскадный режим: включен")

                # close all deals/orders method
                if close_order == 0:
                    # close_order false
                    dict_b["close_order"] = 0
                    print("Режим: Не_закрывать_ордера_сделки")
                else:
                    if close_order == 1:
                        # close_order True
                        dict_b["close_order"] = 1
                        print("Режим: Закрыть_все_сделки")

                print(f"dict_b: {dict_b}")

                dict_a[item[1]] = dict_b        # новый dict

                # --> save new dict to json file
                with open("C:/xampp/htdocs/almaz/files/global_levels.json", 'w') as f:
                    json.dump(dict_a, f, indent=4)  # save new dict_a to json file

        return HttpResponse(f"<h2>Hello, </h2>{high_level_new}")
    else:
        userform = Form_global_levels()
        return render(request, "almaz/input.html", {"form": userform})


# @logger.catch()
def hedge(request):
    """функция представления для Hedge"""

    with open(path_config + 'hedge.json') as f:
        dict_a = json.load(f)
        dict_b = dict_a["EURUSD"]
        sell_stop_price = dict_b["sell_stop_price"]
        buy_stop_price = dict_b["buy_stop_price"]
        cascade_orders = dict_a["cascade_orders"]

    if request.method == "POST":
        today_time = datetime.today().strftime("%d-%m-%Y-%H:%M")  # получим тек время
        dict_a["last_update"] = str(today_time)  # add date/time to dict

        # --- GET VALUES FROM FORM_INPUT
        high_level_new = request.POST.get("high_level")
        low_level_new = request.POST.get("low_level")  # получение значения поля age
        type_order = request.POST.get("type_order")     # получаем тип ордера
        sell_stop_price = request.POST.get("sell_stop_price")   # получаем цену соот-го ордера
        buy_stop_price = request.POST.get("buy_stop_price")
        cascade_orders = request.POST.get("cascade_orders")
        close_positions = request.POST.get("close_positions")
        active = request.POST.get("active")

        # step_1, step_2 = request.POST.get("step_1"), request.POST.get("step_2")
        # step_3, step_4 = request.POST.get("step_3"), request.POST.get("step_4")
        # step_5, step_6 = request.POST.get("step_5"), request.POST.get("step_6")
        # step_7 = request.POST.get("step_7")

        # выбор метода откытия ордера лимитом или stp (пробойные ордера)
        if type_order == "1":
            # limit_order_type = 1
            dict_b["limit_order_type"] = 1
            dict_b["stop_order_type"] = 0
            print(f"ордера на отбой")
            # dict_a["trend"] = trend_new  # присвоим новое значение словаря по ключу login
        elif type_order == "2":
            # stop_order_type = 1
            dict_b["stop_order_type"] = 1
            dict_b["limit_order_type"] = 0
            dict_b["sell_stop_price"] = sell_stop_price
            dict_b["buy_stop_price"] = buy_stop_price
            print(f"ордера на пробой")

        # выбор режима открытия ордеров каскадом
        if cascade_orders == "2":
            print("включен режим cascade")
            dict_a["cascade_orders"] = 1    # включен режим
        elif cascade_orders == "1":
            print("отключен режим cascade")
            dict_a["cascade_orders"] = 0    # отключен режим

        # выбор режима открытия/закрытия открытых позиций
        if close_positions == "1":
            dict_a["close_positions"] = 1
        elif close_positions == "2":
            dict_a["close_positions"] = 0

        # выбор режима включения работы алгоритма или нет
        if active == "1":
            dict_a["active"] = 1
        elif active == "2":
            dict_a["active"] = 0

        # Выбор режима закрытия всех открытх позиций, и активации работы алгоритма
        logger.info(f"close_positions : {close_positions}, active= {active}")

        dict_b["high_level"] = high_level_new.replace(',', '.')  # присвоим новое
        dict_b["low_level"] = low_level_new.replace(',', '.')   # значение словаря по ключу login
        # steps_temp = [step_1, step_2, step_3, step_4, step_5, step_6, step_7]
        # steps_temp_1 = []   # create new empty list for steps

        # если не пустое первое значение step
        # if steps_temp[0] != "":
        #     for step in steps_temp:
        #         if step != "":
        #             step_new = step.replace(',', '.')   # замена ","" на "."
        #             steps_temp_1.append(step_new)       # add new step in list
        #     new_list = [float(i) for i in steps_temp_1]
        #     dict_b["steps"] = new_list          # add new list steps for dict
        # elif steps_temp[0] == "":
        #     pass

        dict_a["EURUSD"] = dict_b     # create new dict with new data
        # logger.info(f"new dict_a: {dict_a}")

        # --> save new dict to json file
        with open(path_config + 'hedge.json', 'w') as f:
            json.dump(dict_a, f, indent=4)  # save new dict_a to json file

        return HttpResponse(f"<h2>Вы ввели данные, {0}</h2>{high_level_new} + {low_level_new}")
    else:
        userform = Hedge_Form()
        return render(request, "almaz/write.html", {"form": userform})


def index_5(request):
    """простая функция представления и редактирования с использованием формы для trade_extremum"""
    trend_new = ""
    with open('C:/xampp/htdocs/almaz/files/trade_extremum.json') as f:
        dict_a = json.load(f)

    if request.method == "POST":
        # now = datetime.now()  # получим тек дату/время
        today_time = datetime.today().strftime("%d-%m-%Y-%H:%M")
        print(f"datetime : {today_time}")
        user_name = request.POST.get("user_name")
        high_level_new = request.POST.get("high_level")  # получаем значения из поля формы high_level
        low_level_new = request.POST.get("low_level")
        trend = request.POST.get("trend")

        print(f"trend: {trend, type(trend)}")
        if trend == "1":
            trend_new = 0   # 0 -> восходящий тренд
            print(f"восходящий тренд")
            # dict_a["trend"] = trend_new  # присвоим новое значение словаря по ключу login
        elif trend == "2":
            trend_new = 1   # -> нисходящий тренд
            print(f"нисходящий тренд")
            # dict_a["trend"] = trend_new  # присвоим новое значение словаря по ключу login

        dict_a["high_level"] = float(high_level_new.replace(',', '.'))  # присвоили новое  полей
        dict_a["low_level"] = float(low_level_new.replace(',', '.'))    # значения для соот-их
        dict_a["trend"] = trend_new  # присвоим новое значение словаря по ключу login
        dict_a["last_update"] = str(today_time)
        # logger.info(f"new dict: {dict}")
        with open('C:/xampp/htdocs/almaz/files/trade_extremum.json', 'w') as f:
            json.dump(dict_a, f, indent=4)  # save new dict to json file

        return HttpResponse(f"<h2>{user_name}, Вы ввели след значения:</h2>"
                            f"high_level: {high_level_new} and low_level: {low_level_new};"
                            f"  Trend: {trend_new}")
    else:
        userform = Form_Trade_Extremum()  # используем нашу форму для данного алгоритма
        return render(request, "almaz/input.html", {"form": userform})


def index_6(request):
    """простая функция представления для вывода итоговых данных из json файлов в html"""
    with open('C:/xampp/htdocs/almaz/files/trade_extremum.json') as f:
        dict_a = json.load(f)

    with open('C:/xampp/htdocs/almaz/files/hedge_martin.json') as d:
        dict_b = json.load(d)
        dict_b_2 = dict_b["EURUSD"]
        high_level, low_level = dict_b_2["high_level"], dict_b_2["low_level"]

    header = "Данные отчета с файлов json"  # обычная переменная
    algorithm = ["Hedge_Martin", "Trade_Extremum"]  # массив
    levels_hedge = [high_level, low_level]
    # dict_a
    name = {"name": "Tom", "age": 23}  # словарь
    addr = ("Абрикосовая", 23, 45)  # кортеж
    data = {"header": header, "algorithm": algorithm, "levels": levels_hedge,
            "trade_extremum": dict_a, "user": name, "address": addr}

    return render(request, "almaz/otchet.html", context=data)


def index_7(request):
    """Главная функция представления в виде таблицы для всех алгоритмов в html + Css"""
    # --> 1. read from json file trade_extremum <-- #
    with open(path_config + 'trade_extremum.json') as f:
        dict_a = json.load(f)
        # dict_b = dict_a["EURUSD"]

    # --> 2. read from json file hedge_martin <--
    with open(path_config + 'hedge.json') as b:
        dict_b = json.load(b)
        dict_b_2 = dict_b["EURUSD"]
        # steps_list = dict_b_2["steps"]

    # --> 3. read from json file global_levels <--
    with open(path_config + 'global_levels.json') as d:
        dict_d = json.load(d)
        symbols_temp = list(dict_d)  # get list of keys from dict_a, list for currency
        symbols_fx = [key for key in symbols_temp if key != "last_update"]  # исключаем не нужные ключи
        # print(f"symbols_fx: {symbols_fx}")

        dict_d_1 = dict_d["GBPUSD"]         # get values from dict_d_1["GBPUSD"]
        dict_d_2 = dict_d["USDCAD"]
        dict_d_3 = dict_d["AUDUSD"]
        dict_d_4 = dict_d["NZDUSD"]

        list_d_1 = list(dict_d_1.values())  # get list of values from dict
        list_d_2 = list(dict_d_2.values())
        list_d_3 = list(dict_d_3.values())
        list_d_4 = list(dict_d_4.values())

    algorithm = ["Hedge_Martin", "Trade_Extremum", "Global_Levels"]  # массив / list

    # name = {"name": "Tom", "age": 23}  # словарь / dict
    data = {"algorithm": algorithm, "trade_extermum": dict_a, "Hedge_Martin": dict_b_2,
            "Last_update": dict_b, "symbols_fx": symbols_fx, "dict_d_1": dict_d_1, "dict_d_2": dict_d_2,
            "dict_d_3": dict_d_3, "dict_d_4": dict_d_4, "list_d_1": list_d_1, "list_d_2": list_d_2,
            "list_d_3": list_d_3, "list_d_4": list_d_4, "dict_d": dict_d}

    return render(request, "almaz/table_algoritms.html", context=data)


def Kovach(request):
    """ Форма ввода параметров для алгоритмов Ковач """
    with open(path_config + 'kovach_signals.json') as f:
        dict_base = json.load(f)
        # dict_eurusd = dict_base["EURUSD"]
    if request.POST.get('action') == 'ajax_post_1':
        # --- GET VALUES FROM FORM_INPUT
        user_name = request.POST.get('user_name')        # from ajax
        regime = request.POST.get('id_regime')        # from ajax
        symbol = request.POST.get('symbol')        # from ajax
        type_order = request.POST.get('type_order')        # from ajax
        open_price_limit = request.POST.get('open_price_limit')        # from ajax
        open_price_stop = request.POST.get('open_price_stop')        # from ajax
        stop_loss_price = request.POST.get('stop_loss_price')        # from ajax
        take_profit_price = request.POST.get('take_profit_price')        # from ajax
        cascade_orders = request.POST.get('cascade_orders')        # from ajax
        active = request.POST.get('active')        # from ajax

        # if request.method == "POST":
        # today_time = datetime.today().strftime("%d-%m-%Y-%H:%M")  # получим тек время
        today_time = datetime.today()      # временно создал
        dict_base["last_update"] = today_time.isoformat("|")  # add date/time to dict

        # active = request.POST.get("active")
        logger.info(f"{regime=}, {user_name=}, {active=}")

        # -- A D D/ U P D A T E  S I G N A L  T O  J S O N  F I L E
        if active == "1":
            dict_base["active"] = '1'
            if symbol and len(symbol) > 1:
                dict_symbol = dict_base[symbol]
                # -- 1. режим открытия позиции
                if regime == "Открытие_позиции":
                    dict_symbol["regime"] = "open_position"
                    dict_symbol["open_price_limit"] = float(open_price_limit)
                    dict_symbol["open_price_stop"] = float(open_price_stop)
                    dict_symbol["stop_loss_price"] = float(stop_loss_price)
                    dict_symbol["take_profit_price"] = float(take_profit_price)
                    dict_symbol["cascade_orders"] = int(cascade_orders)
                    # dict_symbol["cascade_orders"] = int(cascade_orders)

                    if type_order == "Ордера_на_отбой":
                        dict_symbol["limit_order_type"] = 1
                        dict_symbol["stop_order_type"] = 0
                    elif type_order == "Ордера_на_пробой":
                        dict_symbol["limit_order_type"] = 0
                        dict_symbol["stop_order_type"] = 1

                    dict_symbol["last_update"] = today_time.isoformat("|")      # add new code

                    # print(f"проверить : {open_price_stop=}, {type(open_price_stop), (len(open_price_stop))}")
                    dict_base[symbol] = dict_symbol
                    logger.info(f"{dict_symbol=}")

                    with open(path_config + 'kovach_signals.json', 'w') as f:
                        json.dump(dict_base, f, indent=4)  # save new dict to json file

                # -- 2. режим изменения позиции stop_loss/take_profit
                elif regime == "Изменение Stop_loss":
                    dict_symbol["regime"] = "change_position"
                elif regime == "Безубыток по открытым позициям":
                    dict_symbol["regime"] = "breakeven_open_deals"
                elif regime == "Закрытие_позиций":
                    dict_symbol["regime"] = "close_positions"

                    dict_symbol["last_update"] = today_time.isoformat("|")
                    dict_base[symbol] = dict_symbol
                    with open(path_config + 'kovach_signals.json', 'w') as f:
                        json.dump(dict_base, f, indent=4)  # save new dict to json file
                    # logger.info(f"almaz test {path_config=}")

        # print(f"{symbol=}, {regime=}, {type_order=}, {open_price_limit=}, {stop_loss_price=}, {float(take_profit_price)}")
        return HttpResponse(f"<h2> Вы {user_name=} ввели данные для Kovach<br> {dict_base} </h2>")

    else:
        userform = Kovach_Form()
        return render(request, "umbrella/input.html", {"form": userform})
        # return render(request, "almaz/umbrella-co.html", {"form": userform})


def get_expire_data(request):
    """ Форма вывода данных ввиде json """
    with open(path_config + 'users_expire_data.json') as f:
        dict_a = json.load(f)
    # logger.info(f"\ndata: {data}")
    return JsonResponse(dict_a)


def get_kovach_data(request):
    """ Форма вывода данных ввиде json """
    with open(path_config + 'kovach_signals.json') as f:
        dict_a = json.load(f)
    # logger.info(f"\ndata: {data}")
    return JsonResponse(dict_a)
