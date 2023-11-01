from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model


class Profile(models.Model):
    # Поле user со взаимосвязью один-к-одному будет использоваться для
    # ассоциирования профилей с пользователями. С помощью параметра on_
    # delete=models.CASCADE мы принудительно удаляем связанный объект Profile
    # при удалении объекта User.
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/',
                              blank=True)

    def __str__(self):
        return f'Profile of {self.user.username}'


class Contact(models.Model):
    """
    В приведенном выше исходном коде показана модель Contact, которая
        будет использоваться для взаимосвязей пользователей. Она содержит следующие поля:
        • user_from: внешний ключ (ForeignKey) для пользователя, который создает взаимосвязь;
        • user_to: внешний ключ (ForeignKey) для пользователя, на которого есть
        подписка;
        • created: поле DateTimeField с параметром auto_now_add=True для хранения
        времени создания взаимосвязи.
        Для полей ForeignKey индекс базы данных создается автоматически.
         В Metaклассе модели такой индекс определен в убывающем порядке по полю created.
        Также был добавлен атрибут ordering, чтобы сообщать Django
        , что по умолчанию он должен сортировать результаты по полю created. Используя дефис
    перед именем поля, указывается убывающий порядок. Например, -сreated.
    """
    user_form = models.ForeignKey('auth.User',
                                  related_name='rel_from_set',
                                  on_delete=models.CASCADE)
    user_to = models.ForeignKey('auth.User',
                                related_name='rel_to_set',
                                on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['-created']),
        ]
        ordering = ['-created']

    def __str__(self):
        return f'{self.user_form} follows {self.user_to}'


# добавить следующее поле в User динамически
# Здесь модель User извлекается встроенной в  Django типовой функцией
# get_user_model(). Метод add_to_class() моделей Django применяется для того,
# чтобы динамически подправлять модель User
user_model = get_user_model()
user_model.add_to_class('following',
                        models.ManyToManyField('self',
                                               through=Contact,
                                               related_name='followers',
                                               symmetrical=False))
