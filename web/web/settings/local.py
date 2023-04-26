from .base import *

""" Generating secret key: 
python manage.py shell
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
"""
with open(os.path.join(BASE_DIR, 'secret_key.txt')) as f:
    SECRET_KEY = f.read().strip()
    
ALLOWED_HOSTS = []

# Local database scheme
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}    

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]