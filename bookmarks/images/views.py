from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm
from django.shortcuts import get_object_or_404
from .models import Image
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, \
    PageNotAnInteger
from actions.utils import create_action
import redis
from django.conf import settings

# соединение с redis
r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB, )


#  представление image_create был добавлен декоратор login_required, чтобы предотвращать
#  доступ неаутентифицированных пользователей
@login_required
def image_create(request):
    """
        1. Для создания экземпляра формы необходимо предоставить начальные
        данные через HTTP-запрос методом GET. Эти данные будут состоять
        из атрибутов url и title изображения с внешнего веб-сайта.
         Оба параметра будут заданы в запросе GET букмарклетом JavaScript, который
        мы создадим позже. Пока же можно допустить, что эти данные будут
        иметься в запросе.
        2. После того как форма передана на обработку с помощью HTTP-запроса
        методом POST, она валидируется методом form.is_valid(). Если данные
        в форме валидны, то создается новый экземпляр Image путем сохранения формы методом form.save(commit=False).
         Новый экземпляр в базе
        данных не сохраняется, если commit=False.
        3. В новый экземпляр изображения добавляется связь с текущим пользователем,
         который выполняет запрос: new_image.user = request.user. Так
        мы будем знать, кто закачивал каждое изображение.
        4. Объект Image сохраняется в базе данных.
        5. Наконец, с помощью встроенного в Django фреймворка сообщений
        создается сообщение об успехе, и пользователь перенаправляется на
        канонический URL-адрес нового изображения. Мы еще не реализовали
    метод get_absolute_url() модели Image; мы сделаем это позже.
    """
    if request.method == 'POST':
        # Форма отправлена
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            # данные формы валидны
            cd = form.cleaned_data
            new_image = form.save(commit=False)
            # назначить текущего пользователя элементу
            new_image.user = request.user
            new_image.save()
            create_action(request, 'bookmarked image', new_image)
            messages.success(request, 'Image added successfully')
            # перенаправить к представлению детальной
            # информации о только что созданном элементе
            return redirect(new_image.get_absolute_url())
    else:
        # скомпоновать форму с данными,
        # предоставленными букмарклетом методом GET
        form = ImageCreateForm(data=request.GET)
    return render(request,
                  'images/image/create.html',
                  {'section': 'images',
                   'form': form})


def image_detail(request, id, slug):
    # Это представление вывода изображения на страницу
    image = get_object_or_404(Image, id=id, slug=slug)
    # увеличить общее число просмотров изображения на 1
    total_views = r.incr(f'image:{image.id}:views')
    # Увеличить рейтинг изображения на 1
    # Команда zincrby() используется для сохранения просмотров изображений
    # в сортированном множестве с ключом image:ranking. В нем будут храниться
    # id изображения и соответствующий балл, равный 1, который будет добавлен
    # к общему баллу этого элемента сортированного множества. Такой подход
    # позволит отслеживать все просмотры изображений в глобальном масштабе
    # и иметь сортированное множество, упорядоченное по общему числу просмотров.
    r.zincrby('image_ranking', 1, image.id)
    return render(request,
                  'images/image/detail.html',
                  {'section': 'images',
                   'image': image,
                   'total_views': total_views})


# В новом представлении использованы два декоратора. Декоратор login_required
#  не дает пользователям, не вошедшим в систему, обращаться к этому
# представлению. Декоратор require_POST возвращает объект HttpResponseNotAllowed
# (код состояния, равный 405), в случае если HTTP-запрос выполнен не
# методом POST. При таком подходе этому представлению разрешаются запросы только методом POST
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
                create_action(request.user, 'likes', image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except Image.DoesNotExist:
            pass
    return JsonResponse({'status': 'error'})


@login_required
def image_list(request):
    """
    В этом представлении создается набор запросов QuerySet, чтобы извлекать
        все изображения из базы данных. Затем формируется объект Paginator, чтобы
        разбивать результаты на страницы, беря по восемь изображений на страницу.
         Извлекается HTTP GET-параметр page, чтобы получить запрошенный
        номер страницы. Извлекается HTTP GET-параметр images_only, чтобы узнать,
        должна ли прорисовываться вся страница целиком или же только новые
        изображения. Мы будем прорисовывать всю страницу целиком, когда она
        запрашивается браузером. Однако мы будем прорисовывать HTML только
        с новыми изображениями в случае запросов Fetch API, поскольку мы будем
    добавлять их в существующую HTML-страницу.

    В случае HTTP-запросов на JavaScript, которые будут содержать параметр images_only,
    будет прорисовываться шаблон list_images.html. Этот
    шаблон будет содержать изображения только запрошенной страницы;
    • в случае браузерных запросов будет прорисовываться шаблон list.html.
    Этот шаблон будет расширять шаблон base.html, чтобы отображать всю
    страницу целиком, и будет вставлять шаблон list_images.html, который
    будет вставлять список изображений.
    """
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    images_only = request.GET.get('images_only')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым число,
        # то доставить первую страницу
        images = paginator.page(1)
    except EmptyPage:
        if images_only:
            # Если AJAX-запрос и страница вне диапазона,
            # то вернуть пустую страницу
            return HttpResponse('')
        images = paginator.page(paginator.num_pages)
    if images_only:
        return render(request,
                      'images/image/list_images.html',
                      {'section': 'images',
                       'images': images})
    return render(request,
                  'images/image/list.html',
                  {'section': 'images',
                   'images': images})


@login_required
def image_ranking(request):
    # Получить словарь рейтинга изображений
    image_ranking = r.zrange('image_ranking', 0, -1,
                             desc=True)[:10]
    image_ranking_ids = [int(id) for id in image_ranking]
    # получить наиболее просматриваемые изображения
    most_viewed = list(Image.objects.filter(
        id__in=image_ranking_ids))
    most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))
    return render(request,
                  'images/image/ranking.html',
                  {'section': 'images',
                   'most_viewed': most_viewed})
