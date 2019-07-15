from .base import *

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = get_environment_variable(
    "DJANGO_STATIC_ROOT", default_value=os.path.join(BASE_DIR, "static")
)

MEDIA_URL = "/media/"
MEDIA_ROOT = get_environment_variable(
    "DJANGO_MEDIA_ROOT", default_value=os.path.join(BASE_DIR, "media")
)
