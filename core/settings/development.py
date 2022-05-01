from core.settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

STATIC_ROOT = os.path.join(BASE_DIR, 'static_cdn')
STATICFILES_DIRS = [BASE_DIR / 'static']