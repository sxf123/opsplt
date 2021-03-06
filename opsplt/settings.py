"""
Django settings for opsplt project.

Generated by 'django-admin startproject' using Django 1.10.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import djcelery
import string
import random

djcelery.setup_loader()
BROKER_URL = 'amqp://admin:admin@192.168.180.94:5672/vhost'
CELERY_RESULT_BACKEND = 'redis://192.168.180.94:6379/1'
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'm-pga%wvv$*zgwp+$xhq@i$$n^4eqa1uwai8ogr3#5h262^8x-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'common',
    'cmdb',
    'djcelery',
    'rest_framework',
    'rest_framework.authtoken',
    'dj_pagination',
    'application',
    'job',
    'account',
    'database',
    'consul_manage',
    'deployment'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'dj_pagination.middleware.PaginationMiddleware'
]

ROOT_URLCONF = 'opsplt.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages'
            ],
            'libraries': {
                'split_res': 'common.templatetags.split_res',
            }
        },
    },
]

WSGI_APPLICATION = 'opsplt.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'opsplt',
        'USER': 'root',
        'PASSWORD': 'moresec@2020',
        'HOST': '127.0.0.1',
        'PORT': '3306'
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR,'static')

STATICFILES_DIRS = (
    ('assets',os.path.join(STATIC_ROOT,'assets').replace('\\','/')),
    ('plugin',os.path.join(STATIC_ROOT,'plugin').replace('\\','/')),
    ('img',os.path.join(os.path.join(os.path.join(STATIC_ROOT,'plugin'),'css'),'img').replace('\\','/'))
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

JOBID_CHOICE = "abcdefghijklmnopqrstuvwxyz1234567890"

SESSION_COOKIE_AGE = 60 * 60 * 24 * 7 * 2
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SAVE_EVERY_REQUEST = True

AES_ENCRYPT_KEY = "EdKCoeSJz2yDNCA7"

LOGGING = {
    "version" : 1,
    "disable_existing_loggers" : False,
    "formatters" : {
        "standard" : {
            "format" : "%(asctime)s %(levelname)s [ %(message)s] %(pathname)s %(filename)s %(module)s %(funcName)s %(lineno)d"
        },
    },
    "handlers" : {
        "console" : {
            "level" : "INFO",
            "class" : "logging.StreamHandler",
            "formatter" : "standard"
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "handler.log"),
            "formatter": "standard"
        }
    },
    "loggers" : {
        "default" : {
            "handlers" : ["file"],
            "level" : "DEBUG",
            "propagate" : True
        },
        "django_auth_ldap":{
            "handlers":["console"],
            "level":"DEBUG",
            "propatage":True,
        }
    }
}

FLYWAY_BASEDIR = "/opt/flyway"
HARBOR_URL = ""
HARBOR_USERNAME = ""
HARBOR_PASSWORD = ""

SESSION_SAVE_EVERY_REQUEST=True
SESSION_COOKIE_AGE=60*60