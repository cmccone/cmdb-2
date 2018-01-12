"""
Django settings for cmdb project.

Generated by 'django-admin startproject' using Django 1.11.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 't7l)14gc7a3a_^pvj2wfan29kp#la1shmq^=lp*5+&vbyvsqaz'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'repository',
    'django_celery_beat',
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

ROOT_URLCONF = 'cmdb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'web', 'templates')]
        ,
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

WSGI_APPLICATION = 'cmdb.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'web', 'static'),
)

# for celery
CELERY_BROKER_URL = 'amqp://celery:123456@celery:5672/celeryhost'
# CELERY_BROKER_URL = 'redis://192.168.189.132:6379/'
CELERY_RESULT_BACKEND = 'redis://192.168.189.132:6379/'
CELERY_EVENT_QUEUE_TTL = 10
CELERY_EVENT_QUEUE_EXPIRES = 20
CELERY_TASK_RESULT_EXPIRES = 18000
CELERY_result_expires = 100
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ENABLE_UTC = False

CELERY_IMPORTS = (
    'repository.tasks',
)


CELERY_DEFAULT_QUEUE = "default_cmdb"  # 默认的队列，如果一个消息不符合其他的队列就会放在默认队列里面
CELERY_TASK_QUEUES = {
    "default_dongwm": {  # 这是上面指定的默认队列
        "exchange": "default_dongwm",
        "exchange_type": "direct",
        "routing_key": "default_dongwm"
    },
    "topicqueue": {  # 这是一个topic队列 凡是topictest开头的routing key都会被放到这个队列
        "routing_key": "topictest.#",
        "exchange": "topic_exchange",
        "exchange_type": "topic",
    },
    "test2": {  # test和test2是2个fanout队列,注意他们的exchange相同
        "exchange": "broadcast_tasks",
        "exchange_type": "fanout",
        "binding_key": "broadcast_tasks",
    },
    "test": {
        "exchange": "broadcast_tasks",
        "exchange_type": "fanout",
        "binding_key": "broadcast_tasks2",
    },
}


class MyRouter(object):
    def route_for_task(self, name, task=None, args=None, kwargs=None):
        print('name:', name)
        print('task:', task)
        if name.startswith('repository'):
            print('进来了')
            return {
                'queue': 'topicqueue',
                "routing_key": "topictest.abc",
            }
        # 我的dongwm.tasks文件里面有2个任务都是test开头
        elif name.startswith('repository'):
            return {
                "exchange": "broadcast_tasks",
            }
        # 剩下的其实就会被放到默认队列
        else:
            return {
                'queue': 'default_dongwm',
                'routing_key': 'default_dongwm',
            }
# CELERY_ROUTES本来也可以用一个大的含有多个字典的字典,但是不如直接对它做一个名称统配
CELERY_TASK_ROUTES = (MyRouter(),)
