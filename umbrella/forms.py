from django import forms
import json


class Test_Form(forms.Form):
    """для редактирования Kovach
    вводим обязательные поля user_name/high_level/low_level
    steps - вводим если только надо, но редко"""
    user_name = forms.CharField(max_length=30)  # для проверки user по его имени
    type_order = forms.ChoiceField(choices=((1, "Ордера_на_отбой"), (2, "Ордера_на_пробой")))
    buy_limit_price = forms.DecimalField(required=False)  # цена на отбой
    sell_limit_price = forms.DecimalField(required=False)  # цена на отбой

    sell_stop_price = forms.DecimalField(required=False)  # цена для sell ордера на пробой
    buy_stop_price = forms.DecimalField(required=False)  # цена для buy ордера на пробой

    stop_loss = forms.IntegerField(required=True)  # размер стопа в пунктах/пипсах
    take_profit = forms.DecimalField(required=False)

    cascade_orders = forms.ChoiceField(choices=((1, "Каскадные_ордера_отключены"), (2, "Каскадные_ордера_включены")),
                                       required=False)
    close_positions = forms.ChoiceField(choices=((1, "Закрыть все открытые позиции"), (2, "Ничего не закрывать")),
                                        required=False)
    close_orders = forms.ChoiceField(choices=((1, "Ничего не закрывать"), (2, "Закрыть все отложенные ордера")),
                                     required=False)
    active = forms.ChoiceField(choices=((1, "Включить работу алгоритма"), (2, "Выключить алгоритм")),
                               required=False)
