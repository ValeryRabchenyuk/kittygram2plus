"""
В Django REST Framework все классы разрешений наследуются от базового класса BasePermission.
В нём описаны два метода:
    —  has_permission определяются разрешения на уровне запроса; обладает информацией о запросе.
    —  has_object_permission устанавливаются разрешения на уровне объекта. обладает информацией о запросе и об объекте запроса.

class BasePermission(metaclass=BasePermissionMetaclass):

    # Определяет права на уровне запроса и пользователя
    def has_permission(self, request, view):
        return True

    # Определяет права на уровне объекта
    def has_object_permission(self, request, view, obj):
        return True 

Чтобы создать собственное разрешение — нужно описать свой класс, расширяющий BasePermission, и переопределить один или оба его метода.

has_object_permission:
        —— никогда не выполняется для представлений, возвращающих коллекции объектов или создающих новый объект модели
        —— вызывается только в том случае, если has_permission вернул True. 
            По умолчанию оба метода возвращают значение True. 
            Поэтому если в кастомном пермишене не переопределить эти методы — пользователям будет предоставлен полный доступ.
"""


from rest_framework import permissions


class OwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        """"проверяется метод запроса и статус пользователя. 
        сли метод запроса безопасный (то есть GET, HEAD или OPTIONS) 
        или если пользователь аутентифицирован (то есть предоставил валидный токен), 
        то метод вернёт True.
        """
        return (
                request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
            )

    def has_object_permission(self, request, view, obj):
        """"
        передаётся запрошенный объект, и теперь в этом методе можно проверить, 
        совпадает ли автор объекта с пользователем из запроса.
        """
        return obj.owner == request.user
    
    
class ReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS