"""
Django settings for bookmarks project.

Generated by 'django-admin startproject' using Django 4.1.12.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-7+8r_rolm&-ubfyx(2r^q+vg1kw@4h^2h8$eow0vrx=)hb!bfr'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'account.apps.AccountConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bookmarks.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'bookmarks.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# LOGIN_REDIRECT_URL: сообщает Django URL-адрес, на который следует перенаправлять
# пользователя после успешного входа, если в запросе нет
# параметра next;
LOGIN_REDIRECT_URL = 'dashboard'

# LOGIN_URL: URL-адрес, на который следует перенаправлять пользователя
# чтобы зарегистрировать его вход (например, представления, в которых
# используется декоратор login_required);
LOGIN_URL = 'login'

#  LOGOUT_URL: URL-адрес, на который следует перенаправлять пользователя, чтобы зарегистрировать его выход.
LOGOUT_URL = 'logout'

# Настроечный параметр EMAIL_BACKEND указывает класс, который будет использоваться для отправки электронной почты.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

#  MEDIA_URL – это базовый URL-адрес,
# используемый для раздачи медиафайлов, закачанных пользователями на сайт.
MEDIA_URL = 'media/'

# MEDIA_ROOT – это локальный путь, где они находятся. Пути и URL-адреса файлов
# формируются динамически посредством добавления к ним пути проекта или
# URL-адреса медиафайлов в качестве префикса с целью переносимости.
MEDIA_ROOT = BASE_DIR / 'media'

# В данном настроечном параметре мы оставляем стандартный ModelBackend,
# который используется для аутентификации с помощью пользовательского имени
# и пароля, и вставляем наш собственный бэкенд аутентификации
# с применением электронной почты EmailAuthBackend
AUTHENTICATION_BACKENDS = [
 'django.contrib.auth.backends.ModelBackend',
 'account.authentication.EmailAuthBackend',
]
