"""
Django settings for NewsPaper project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
import logging
import sys
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-7+yd1*r=&rdndz5r&qcgbo#0emy0cmfa-s$@=t4khu4)%34fsk'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []#['127.0.0.1', 'localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    'django.contrib.sites',
    'news.apps.NewsConfig',
    'accounts',
    'django_filters',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.yandex',
    'subscriptions',
    'django_apscheduler',

]

SITE_ID = 1
LOGIN_REDIRECT_URL = "/news"
LOGOUT_REDIRECT_URL = '/news'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware', #добавлено для локализации
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'base_format': {
            'format': '%(asctime)s :: %(levelname)-6s @@@ %(message)s'
        },
        'warning_format': {
            'format': '%(asctime)s :: %(levelname)-6s @@@ %(message)s @@@ %(pathname)s'
        },
        'error_format': {
            'format': '{asctime} уровень:{levelname} сообщение:{message} путь:{pathname} стек ошибки:{exc_info}',
            'style': '{',
        },
        'error_email_format': {
            'format': '%(asctime)s уровень:%(levelname)s сообщение:%(message)s путь:%(pathname)s',
        },
        'info_format': {
            'format': '{asctime} :: {levelname} :: {module}',
            'style': '{',
        },
        'security_format': {
            'format': '{asctime} :: {levelname} :: {module} :: {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'base_format',
            'filters': ['require_debug_true']
        },
        'console_warning': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'warning_format',
            'filters': ['require_debug_true']
        },
        'console_error': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'error_format',
            'filters': ['require_debug_true']
        },
        'general': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'info_format',
            'filters': ['require_debug_false'],
            'filename': 'general.log',
        },
        'errors1': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'formatter': 'error_format',
            'filename': 'errors.log',
        },
        'security': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'security_format',
            'filename': 'security.log',
        },
        'mail_admins': { #На почту не отправляется, т/к/ удален пароль почты. Настройки логгера отправки на почту считаю настроенным верно
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'formatter': 'error_email_format',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
    },
    'loggers': {
        'django': {
            'level': 'DEBUG',
            'handlers': ['console', 'console_warning', 'console_error', 'general'],
            'propagate': True
        },
        'django.request': {
            'level': 'ERROR',
            'handlers': ['errors1', 'mail_admins'],
            'propagate': False
        },
        'django.server': {
            'level': 'ERROR',
            'handlers': ['errors1', 'mail_admins'],
            'propagate': False
        },
        'django.template': {
            'level': 'ERROR',
            'handlers': ['errors1'],
            'propagate': False
        },
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['errors1'],
            'propagate': False
        },
        'django.security': {
            'level': 'INFO',
            'handlers': ['security'],
            'propagate': False
        }
    }
}

ROOT_URLCONF = 'NewsPaper.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

WSGI_APPLICATION = 'NewsPaper.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_FORMS = {"signup": "accounts.forms.CustomSignupForm"}

# SOCIALACCOUNT_FORMS = {'signup': 'accounts.forms.CustomSocialSignupForm'}
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' #Настроен вывод в консоль, т.к. удален пароль в settings от почты
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = "wisears"
EMAIL_HOST_PASSWORD = ""
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_SUBJECT_PREFIX = 'AUTO_MESSAGE_TO_MNGR! '
SITE_URL = 'http://127.0.0.1:8000'

APSCHEDULER_DATETIME_FORMAT = 'N j, Y f:s a'
APSCHEDULER_RUN_NOW_TIMEOUT = 25

DEFAULT_FROM_EMAIL = "wisears@yandex.ru"
SERVER_EMAIL = "wisears@yandex.ru"
MANAGERS = (
    ('wise_air', 'wise_air@list.ru'),
    ('prodpartner', 'prodpartner@yandex.ru'),
)
ADMINS = (
    ('wisears', 'wisears@yandex.ru'))

CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Yekaterinburg'

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Asia/Yekaterinburg'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = [
    BASE_DIR / "static"
]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_files'),
        # Указываем, куда будем сохранять кэшируемые файлы!
        # Не забываем создать папку cache_files внутри папки с manage.py!
    }
}
