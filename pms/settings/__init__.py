import os

APP_ENV = os.environ.get('APP_ENV', 'development')

if APP_ENV in ('development', 'staging', 'production'):
    exec(f'from .base import *')
    exec(f'from .{APP_ENV} import *')
else:
    raise Exception("Invalid APP_ENV configuration, Expected one of development, staging, production")
