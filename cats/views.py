
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.throttling import AnonRateThrottle
from rest_framework.throttling import ScopedRateThrottle  # см. сеттингз — собственный лимит запросов
from rest_framework.pagination import PageNumberPagination # пагинация для отдельного view-класса 
from django_filters.rest_framework import DjangoFilterBackend   # фильтрация запроса

from .models import Achievement, Cat, User

from .throttling import WorkingHoursRateThrottle # кастомный лимит

from .serializers import AchievementSerializer, CatSerializer, UserSerializer
from .permissions import OwnerOrReadOnly, ReadOnly
from rest_framework import filters


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
       # Устанавливаем разрешение, в сеттингыс.ру стоит IsAuthenticated
       # анонимный доступ на чтение — только к котикам, к другим данным — по токену. 

       # У разрешений на уровне проекта приоритет ниже, чем у разрешений на уровне представления.
    #    У разрешений на одном уровне, тоже есть приоритеты: у более строгих приоритет выше. 
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)   ЗАМЕНИЛИ НА КАСТОМНЫЙ
    permission_classes = (OwnerOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)  # фильтрация запроса
    pagination_class = PageNumberPagination    # параметр PAGE_SIZE будет взят из словаря REST_FRAMEWORK в settings.py.

                                               # Если пагинация установлена на уровне проекта, 
                                               # то для отдельного класса её можно отключить, установив pagination_class = None. 
    Второй вариант пагинации:
    # Даже если на уровне проекта установлен PageNumberPagination
    # Для котиков будет работать LimitOffsetPagination (более гибкий )
    pagination_class = LimitOffsetPagination 

    Третий вариант пагинации:
    # Вот он наш собственный класс пагинации с page_size=20
    pagination_class = CatsPagination 
    filterset_fields = ('color', 'birth_year')
    search_fields = ('name',)
    ordering_fields = ('name', 'birth_year') 
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