from .base import *
import dj_database_url

SECRET_KEY = 'rj3dpu8-^0o0--bfjh4(wqiw0lrw67dze4bl%q#dj=ts4jp0(n'

DEBUG = True

ALLOWED_HOSTS = ['phoenix-pms.herokuapp.com']


DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        'CONFIG': {
            'hosts': [os.getenv('REDIS_URL')]
        }
    }
}