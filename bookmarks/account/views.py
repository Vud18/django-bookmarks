from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile, Contact
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST


@login_required
def edit(request):
    # Мы добавили новое представление edit, чтобы пользователи могли редактировать свою личную информацию.
    # Мы добавили в него декоратор login_required, поскольку только аутентифицированные пользователи могут
    # редактировать свои профили. В этом представлении используются две модельные
    # формы: UserEditForm для хранения данных во встроенной модели
    # User и ProfileEditForm для хранения дополнительных персональных данных
    # в конкретно-прикладной модели Profile. В целях валидации переданных
    # данных вызывается метод is_valid() обеих форм. Если обе формы содержат
    # валидные данные, то обе формы сохраняются путем вызова метода save(),
    # чтобы обновить соответствующие объекты в базе данных.
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Профиль обновлен успешно!')
        else:
            messages.error(request, 'Ошибка обновления профиля')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})


def register(request):
    # Представление создания учетных записей пользователей
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Создать новый объект пользователя,
            # но пока не сохранять его
            new_user = user_form.save(commit=False)
            # установить выбраный пароль
            # set_password Данный метод хеширует пароль перед его сохранением в базе
            # данных
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Сохранить объект User
            new_user.save()
            # Создать профиль пользователя
            Profile.objects.create(user=new_user)
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()

    return render(request,
                  'account/register.html',
                  {'user_form': user_form})


@login_required
# Декоратор login_required проверяет аутентификацию текущего пользователя.
# Если пользователь аутентифицирован, то оно исполняет декорированное
# представление; если пользователь не аутентифицирован, то оно перенаправляет
# пользователя на URL-адрес входа с изначально запрошенным URL-адресом в качестве GET-параметра с именем next.
def dashboard(request):
    # Мы также определили переменную section.
    # Эта переменная будет использоваться для подсвечивания текущего раздела в главном меню сайта.
    return render(request,
                  'account/dashboard.html',
                  {'selection': 'dashboard'})


def user_login(request):
    #  authenticate() и login(): authenticate()
    # проверяет учетные данные пользователя и возвращает объект User, если они
    # правильны; login() задает пользователя в текущем сеансе.
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'],)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Аутентификация прошла успешно')
                else:
                    return HttpResponse('Отключенная учетная запись')
            else:
                return HttpResponse('Неверный логин или пароль')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


#  Представление user_list получает всех активных пользователей.
# Модель User содержит флаг is_active, который маркирует, считается учетная
# запись пользователя активной или нет. Запрос фильтруется по параметру
# is_active=True, чтобы возвращать только активных пользователей.
# Это представление возвращает все результаты, но его можно улучшить,
# добавив постраничную разбивку так же, как это делалось для представления image_list.
@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request,
                  'account/user/list.html',
                  {'section': 'people',
                   'users': users})


# В представлении user_detail используется функция сокращенного доступа
# get_object_or_404(), чтобы извлекать активного пользователя с переданным
# пользовательским именем (username). Данное представление возвращает
# HTTP-ответ 404, если активный пользователь с переданным пользовательским именем не найден
@login_required
def user_detail(request, username):
    user = get_object_or_404(User,
                             username=username,
                             is_active=True)
    return render(request,
                  'account/user/detail.html',
                  {'section': 'people',
                   'user': user})


@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(
                    user_form=request.user,
                    user_to=user)
            else:
                Contact.objects.filter(user_form=request.user,
                                       user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'error'})
