from django import forms
import json


class Hedge_Form(forms.Form):
    """для редактирования Hedge
    вводим обязательные поля user_name/high_level/low_level
    steps - вводим если только надо, но редко"""
    user_name = forms.CharField(max_length=30)  # для проверки user по его имени
    high_level = forms.DecimalField(decimal_places=5)
    low_level = forms.DecimalField(decimal_places=5)

    type_order = forms.ChoiceField(choices=((1, "Ордера_на_отбой"), (2, "Ордера_на_пробой")))
    sell_stop_price = forms.DecimalField(decimal_places=5, required=False)  # цена для sell ордера лимитный на пробой
    buy_stop_price = forms.DecimalField(decimal_places=5, required=False)  # цена для buy ордера лимитный на пробой

    cascade_orders = forms.ChoiceField(choices=((1, "Каскадные_ордера_отключены"), (2, "Каскадные_ордера_включены")),
                                       required=False)

    close_positions = forms.ChoiceField(choices=((1, "Закрыть все открытые позиции"), (2, "Ничего не закрывать")),
                                        required=False)
    active = forms.ChoiceField(choices=((1, "Включить работу алгоритма"), (2, "Выключить алгоритм")),
                               required=False)

    # step_1 = forms.DecimalField(decimal_places=5, required=False)   # шаги для сетки ордеров
    # step_2 = forms.DecimalField(decimal_places=5, required=False)   # алгоритма мартингейл
    # step_3 = forms.DecimalField(decimal_places=5, required=False)   # не обязательные поля
    # step_4 = forms.DecimalField(decimal_places=5, required=False)   # для ввода т.к редко меняем steps
    # step_5 = forms.DecimalField(decimal_places=5, required=False)
    # step_6 = forms.DecimalField(decimal_places=5, required=False)
    # step_7 = forms.DecimalField(decimal_places=5, required=False)


class Form_Trade_Extremum(forms.Form):
    """для редактирования Trade_extremum"""
    user_name = forms.CharField(max_length=30)  # для проверки user по его имени
    high_level = forms.DecimalField(decimal_places=5)
    low_level = forms.DecimalField(decimal_places=5)
    # trend = forms.CharField(label='Введите:', initial="up", help_text='up or down',
    #                         min_length=2, max_length=4)
    trend = forms.ChoiceField(choices=((1, "up"), (2, "down")))


class Form_global_levels(forms.Form):
    """для редактирования global_levels"""
    user_name = forms.CharField(max_length=30)  # для проверки user по его имени
    currency = forms.ChoiceField(choices=((1, "GBPUSD"), (2, "USDCAD"), (3, "AUDUSD"), (4, "NZDUSD")))
    high_level = forms.DecimalField(decimal_places=5)
    low_level = forms.DecimalField(decimal_places=5)
    stop_loss_pips = forms.IntegerField()  # для размера стопа

    CHOICES = [('1', 'Limit_ордера_включены'), ('2', 'Stop_ордера_включены')]
    type_order = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

    sell_stop_price = forms.DecimalField(decimal_places=5)
    buy_stop_price = forms.DecimalField(decimal_places=5)
    cascade_orders = forms.ChoiceField(choices=((0, "Каскадные_ордера_отключены"), (1, "Каскадные_ордера_включены")),
                                       required=False)

    close_order = forms.ChoiceField(choices=((0, "Не_закрывать_ордера_сделки"), (1, "Закрыть_все_сделки")),
                                    required=False)  # для закрытия сделки/сделок


class Kovach_Form(forms.Form):
    """для редактирования Kovach
    вводим обязательные поля user_name/high_level/low_level
    steps - вводим если только надо, но редко"""
    user_name = forms.CharField(max_length=30)  # для проверки user по его имени
    regime = forms.ChoiceField(choices=(("Открытие позиции", "Открытие позиции"), ("Изменение Stop_loss", "Изменение Stop_loss"),
                                        ("Безубыток по открытым позициям", "Безубыток по открытым позициям"), ("Закрытие позиций", "Закрытие позиций")))
    symbol = forms.ChoiceField(choices=(("EURUSD", "EURUSD"), ("GBPUSD", "GBPUSD"), ("AUDUSD", "AUDUSD"), ("USDCAD", "USDCAD"),
                                        ("GOLD", "GOLD"), ("NZDUSD", "NZDUSD"), ("USDJPY", "USDJPY"), ("BRENT", "BRENT")))
    type_order = forms.ChoiceField(choices=(("Ордера_на_отбой", "Ордера_на_отбой"), ("Ордера_на_пробой", "Ордера_на_пробой")))
    open_price_limit = forms.DecimalField(required=False)  # цена открытия позиции/цена отложки ОТБОЙ
    open_price_stop = forms.DecimalField(required=False)  # цена для ордера на пробой

    stop_loss_price = forms.DecimalField(required=False)      # цена stop loss для данного инструмента
    take_profit_price = forms.DecimalField(required=False)    # цена take_profit для данного инструмента

    cascade_orders = forms.ChoiceField(choices=((0, "Каскадные_ордера_отключены"), (1, "Каскадные_ордера_включены")),
                                       required=False)
    active = forms.ChoiceField(choices=(("Алгоритм Включен", "Алгоритм Включен"), (2, "Алгоритм Отключен")),
                               required=False)
