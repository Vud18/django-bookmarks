from django.contrib.auth.models import User


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
