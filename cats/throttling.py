"""
Кастомные тротлинг-классы.

Наследуются от базового класса BaseThrottle,
в наследнике описывают метод allow_request — 
он должен возвращать True, если нужно разрешить запрос,
и False — если запрос следует отклонить.
"""


import datetime

from rest_framework import throttling


class WorkingHoursRateThrottle(throttling.BaseThrottle):
    """
    Админы сервера попросили выделить им 2 часа в сутки (с трёх до пяти утра)
    на нагрузочное тестирование запросов к котикам.
    Просят на это время запретить обработку запросов. 
    В остальное время число обрабатываемых запросов должно лимитироваться, как и прежде.
    """

    def allow_request(self, request, view):
        now = datetime.datetime.now().hour
        if now >= 3 and now < 5:
            return False
        return True