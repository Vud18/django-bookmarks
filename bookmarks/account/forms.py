from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UserEditForm(forms.ModelForm):
    # serEditForm позволит пользователям редактировать свое имя, фамилию
    # и адрес электронной почты, которые являются атрибутами встроенной
    # в Django модели User;
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    # В данном случае мы добавили валидацию поля email, чтобы пользователи
    # не могли изменять свой бывший адрес электронной почты на существующий
    # адрес электронной почты другого пользователя
    def clean_email(self):
        data = self.cleaned_data['email']
        qs = User.objects.exclude(id=self.instance.id)\
            .filter(email=data)
        if qs.exists():
            raise forms.ValidationError('Почта уже используется')
        return data


class ProfileEditForm(forms.ModelForm):
    # ProfileEditForm позволит пользователям редактировать данные профиля,
    # сохраненные в конкретно-прикладной модели Profile. Пользователи смогут
    # редактировать дату своего рождения и закачивать изоражение на сайт в качестве фотоснимка профиля.
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo']


class LoginForm(forms.Form):
    # Приведенная выше форма будет использоваться для аутентификации
    # пользователей по базе данных. Обратите внимание, что для прорисовки
    # HTML-элемента password используется виджет PasswordInput. Такой подход
    # позволит вставлять type="password" в HTML, чтобы браузер воспринимал его
    # как ввод пароля.
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    # Здесь была создана модельная форма для модели пользователя. Данная
    # форма содержит поля username, first_name и email модели User. Указанные
    # поля будут валидироваться в соответствии с проверками на валидность соответствующих полей модели
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password']

    # добавили валидацию поля электронной почты, которая не позволяет
    # пользователям регистрироваться с уже существующим адресом электронной
    # почты.
    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Пользователь с таким почтовым адресов уже есть!')
        return data
