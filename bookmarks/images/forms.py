from django import forms
from .models import Image
from django.core.files.base import ContentFile
from django.utils.text import slugify
import requests


class ImageCreateForm(forms.ModelForm):
    """
    Мы определили форму ModelForm из модели Image, включая только поля title, url и description.
     Пользователи не будут вводить URL-адрес изображения
    прямо в форму. Вместо этого мы предоставим им инструмент JavaScript,
     который позволит им выбирать изображение с внешнего сайта, а форма будет
    получать URL-адрес изображения в качестве параметра. Мы переопределили
    стандартный виджет поля url, чтобы использовать виджет HiddenInput. Этот
    виджет прорисовывается как HTML-элемент input с атрибутом type="hidden".
    Мы используем данный виджет, потому что не хотим, чтобы это поле было
    видимым для пользователя
    """

    class Meta:
        model = Image
        fields = ['title', 'url', 'description']
        widgets = {
            'url': forms.HiddenInput,
        }

    def clean_url(self):
        """
        Для того чтобы убедиться, что предоставленный URL-адрес изображения является валидным,
         мы проверим, что имя файла заканчивается расширением
        .jpg, .jpeg либо .png, чтобы разрешить делиться только файлами JPEG и PNG.

        1) значение поля url извлекается путем обращения к словарю clean_data
        экземпляра формы;
        2) URL-адрес разбивается на части, чтобы проверить наличие валидного
        расширения у файла. Если расширение невалидно, то выдается ошибка
        ValidationError, и экземпляр формы не валидируется.
        """
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg', 'png']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError('Данный URL-адрес не соответствует'
                                        ' действительным расширениям изображений')
        return url

    def save(self, force_insert=False,
             force_update=False,
             commit=True):
        """
        Мы переопределили метод save(), сохранив параметры, требуемые классом ModelForm. Приведенный выше
         исходный код объясняется следующим
        образом.
        1. Новый экземпляр изображения создается путем вызова метода save()
        формы с commit=False.
        2. URL-адрес изображения извлекается из словаря clean_data формы.
        3. Имя изображения генерируется путем комбинирования названия изображения с изначальным расширением файла изображения.
        4. Библиотека Python requests используется для скачивания изображения путем отправки HTTP-запроса методом GET с
         использованием URL-адреса изображения. Ответ сохраняется в объекте response.
        5. Вызывается метод save() поля image, передавая ему объект ContentFile,
        экземпляр которого заполнен содержимым скачанного файла. Таким
        путем файл сохраняется в каталог media проекта. Параметр save=False
        передается для того, чтобы избежать сохранения объекта в базе данных.
        6. Для того чтобы оставить то же поведение, что и в изначальном методе save()
         модельной формы, форма сохраняется в базе данных только
        в том случае, если параметр commit равен True.
        """
        image = super().save(commit=False)
        image_url = self.cleaned_data['url']
        name = slugify(image.title)
        extension = image_url.rsplit('.', 1)[1].lower()
        image_name = f"{name}.{extension}"

        # скачать изображения с данного URL-адреса
        response = requests.get(image_url)
        image.image.save(image_name,
                         ContentFile(response.content),
                         save=False)
        if commit:
            image.save()
        return image
