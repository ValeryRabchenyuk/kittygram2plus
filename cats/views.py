
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.throttling import AnonRateThrottle
from rest_framework.throttling import ScopedRateThrottle  # см. сеттингз — собственный лимит запросов


from .models import Achievement, Cat, User

from .throttling import WorkingHoursRateThrottle # кастомный лимит

from .serializers import AchievementSerializer, CatSerializer, UserSerializer
from .permissions import OwnerOrReadOnly, ReadOnly


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
       # Устанавливаем разрешение, в сеттингыс.ру стоит IsAuthenticated
       # анонимный доступ на чтение — только к котикам, к другим данным — по токену. 

       # У разрешений на уровне проекта приоритет ниже, чем у разрешений на уровне представления.
    #    У разрешений на одном уровне, тоже есть приоритеты: у более строгих приоритет выше. 
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)   ЗАМЕНИЛИ НА КАСТОМНЫЙ
    permission_classes = (OwnerOrReadOnly,)
    # throttle_classes = (AnonRateThrottle,)  # Подключили класс AnonRateThrottle — базовый лимит для анонимов
                                              # Для view-функций есть декоратор @throttle_classes():
                                              # он принимает на вход классы из rest_framework.throttling. 

    # Если кастомный тротлинг-класс вернёт True - запросы будут обработаны
    # Если он вернёт False - все запросы будут отклонены
    throttle_classes = (WorkingHoursRateThrottle, ScopedRateThrottle)

    throttle_scope = 'low_request'          # кастомный лимит,  'low_request'  —  кастомное имя (ключ) из сеттингз

    def get_permissions(self):
        """
        Теперь при GET-запросе информации о конкретном котике
        доступ будет определяться пермишеном ReadOnly: 
        запросы будут разрешены всем. 
        При остальных запросах доступ будет определять пермишен OwnerOrReadOnly.
        """
        # Если в GET-запросе требуется получить информацию об объекте
        if self.action == 'retrieve':
            # Вернём обновлённый перечень используемых пермишенов
            return (ReadOnly(),)
        # Для остальных ситуаций оставим текущий перечень пермишенов без изменений
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user) 


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer