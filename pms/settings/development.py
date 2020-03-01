import os
from .base import BASE_DIR

SECRET_KEY = 'rj3dpu8-^0o0--bfjh4(wqiw0lrw67dze4bl%q#dj=ts4jp0(n'

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
