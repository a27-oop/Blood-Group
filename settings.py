from lifelink.settings import BASE_DIR


INSTALLED_APPS = [
    
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts.apps.AccountsConfig',
    'donor',
    'requestsystem',
    'ai_validation',]

STATIC_URL = 'static/'

STATICFILES_DIRS = [ BASE_DIR / "static"
]