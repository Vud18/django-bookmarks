from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse


class Image(models.Model):
    """
        Это модель, которая будет использоваться для хранения изображений на
            платформе.
                • user: здесь указывается объект User, который сделал закладку на это
            изображение. Это поле является внешним ключом, поскольку оно определяет взаимосвязь один-ко-многим:
             пользователь может отправлять
            несколько изображений, но каждое изображение отправляется одним
            пользователем. Мы использовали CASCADE для параметра on_delete, чтобы связанные изображения удалялись при удалении
             пользователя;
            • title: заголовок изображения;
            • slug: короткое обозначение, содержащее только буквы, цифры, подчеркивания или дефисы, которое будет
             использоваться для создания
            красивых дружественных для поисковой оптимизации URL-адресов;
            • url: изначальный URL-адрес этого изображения. Мы используем max_
            length, чтобы определить максимальную длину, равную 2000 символов;
            • image: файл изображения;
            • description: опциональное описание изображения;
            • created: дата и время, когда объект был создан в базе данных. Мы добавили auto_now_add,
         чтобы устанавливать текущее время/дату автоматически при создании объекта.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='images_created',
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,
                            blank=True)
    url = models.URLField(max_length=2000)
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    # В данном случае понадобится взаимосвязь многие-ко-многим, поскольку пользователю может
    # нравиться несколько изображений, и каждое изображение может нравиться
    # нескольким пользователям.
    # При определении поля ManyToManyField Django создает промежуточную таблицу соединения,
    # используя первичные ключи обеих моделей.
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='images_liked',
                                        blank=True)

    class Meta:
        # Индексы базы данных повышают производительность запросов.
        # Рассмотрите возможность создания индексов для полей, которые часто запрашиваются
        # методами filter(), exclude() или order_by().
        # Поля ForeignKey либо поля с параметром unique=True подразумевают создание индекса.
        indexes = [
            models.Index(fields=['-created']),
        ]
        ordering = ['-created']

    def save(self, *args, **kwargs):
        # Если при сохранении объекта Image поле slug является пустым,
        # то slug генерируется автоматически из поля title изображения с помощью функции
        # slugify(). Затем объект сохраняется. Благодаря автоматическому генерированию
        # слага из заголовка пользователям не придется указывать слаг, когда
        # они делятся изображениями на сайте.
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        # общепринятым способом предоставления канонических
        # URL-адресов объектам является определение метода get_absolute_url() в модели
        return reverse('images:detail', args=[self.id,
                                              self.slug])

    def __str__(self):
        return self.title
