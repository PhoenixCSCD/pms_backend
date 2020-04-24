import os
from .base import BASE_DIR

SECRET_KEY = 'rj3dpu8-^0o0--bfjh4(wqiw0lrw67dze4bl%q#dj=ts4jp0(n'

DEBUG = True

ALLOWED_HOSTS = ['jkakabo.pythonanywhere.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'jkakabo$pms',
        'HOST': 'jkakabo.mysql.pythonanywhere-services.com',
        'PORT': '3306',
        'USER': 'jkakabo',
        'PASSWORD': 'neutron45'
    }
}
