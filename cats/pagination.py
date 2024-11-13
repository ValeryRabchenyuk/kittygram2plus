"""
Кастомный пагинатор наследуют от подходящего встроенного класса или от базового BasePagination.
Его можно указывать в настройках пагинации во вьюсетах, дженериках или в глобальных настройках проекта.
"""

from rest_framework.pagination import PageNumberPagination


class CatsPagination(PageNumberPagination):
    page_size = 20



"""
Методы paginate_queryset и get_paginated_response
В базовом классе пагинаторов BasePagination определены два метода:
    —   paginate_queryset(self, queryset, request, view=None): в него передаётся исходный queryset, 
            а возвращает он итерируемый объект, содержащий только данные запрашиваемой страницы;
    —   get_paginated_response(self, data): принимает сериализованные данные страницы, 
            возвращает экземпляр Response.

"""