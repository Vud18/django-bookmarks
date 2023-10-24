from django import forms


class LoginForm(forms.Form):
    # Приведенная выше форма будет использоваться для аутентификации
    # пользователей по базе данных. Обратите внимание, что для прорисовки
    # HTML-элемента password используется виджет PasswordInput. Такой подход
    # позволит вставлять type="password" в HTML, чтобы браузер воспринимал его
    # как ввод пароля.
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
