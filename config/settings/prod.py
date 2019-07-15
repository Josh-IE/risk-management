from .base import *

# Application definition

INSTALLED_APPS += ("django_s3_storage",)

YOUR_S3_BUCKET = get_environment_variable("STATIC_S3_BUCKET")

DEFAULT_FILE_STORAGE = "django_s3_storage.storage.S3Storage"
STATICFILES_STORAGE = "django_s3_storage.storage.StaticS3Storage"
AWS_S3_BUCKET_NAME_STATIC = AWS_S3_BUCKET_NAME = YOUR_S3_BUCKET

# These next two lines will serve the static files directly
# from the s3 bucket
AWS_S3_CUSTOM_DOMAIN = "%s.s3.amazonaws.com" % AWS_S3_BUCKET_NAME
STATIC_URL = MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
