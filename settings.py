from lifelink.settings import BASE_DIR


INSTALLED_APPS = [
    
    'accounts',
    'donor',
    'requestsystem',
    'ai_validation',]

STATIC_URL = 'static/'

STATICFILES_DIRS = [ BASE_DIR / "static"
]