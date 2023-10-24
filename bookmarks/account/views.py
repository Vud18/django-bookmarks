from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm


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
