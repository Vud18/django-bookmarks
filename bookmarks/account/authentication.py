from django.contrib.auth.models import User

from account.models import Profile


def create_profile(backend, user, *args, **kwargs):
    """
    Создать профиль пользователя для социальной аутентификации.
     Функции create_profile проверяется наличие объекта user и используется метод get_or_create(),
      чтобы отыскивать объект Profile для данного
    пользователя, создавая его при необходимости.
    """
    # Функция, которая создает объект Profile в базе данных при каждом
    # формировании нового пользователя. Затем мы добавим эту
    # функцию в конвейер социальной аутентификации

    # Backend: используемый для аутентификации пользователей бэкенд
    # социальной аутентификации. Напомним, что вы добавили бэкенды социальной
    # аутентификации в настроечный параметр AUTHENTICATION_BACKENDS проекта;

    # user: экземпляр класса User нового либо существующего пользователя,
    # прошедшего аутентификацию

    Profile.objects.get_or_create(user=user)


class EmailAuthBackend:
    """
    Аутентифицировать посредством адреса электронной почты
    """
    # Authenticate(): извлекается пользователь с данным адресом электронной почты,
    # а пароль проверяется посредством встроенного метода
    # check_password() модели пользователя. Указанный метод хеширует пароль,
    # чтобы сравнить данный пароль с паролем, хранящимся в базе
    # данных. Отлавливаются два разных исключения, относящихся к набору
    # запросов QuerySet: DoesNotExist и MultipleObjectsReturned
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
