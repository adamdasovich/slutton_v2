import os
from .settings import *
import dj_database_url

# SECURITY SETTINGS
DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-x(k9bxn)apemzuq9#jcq447-wv4gm@$bl&uup9nnu6$l&&_fvc')
ALLOWED_HOSTS = [
    'louisslutton.com',
    'www.louisslutton.com',
    'api.louisslutton.com',
    '.railway.app',
    '.up.railway.app',
]

# CORS Settings
CORS_ALLOWED_ORIGINS = [
    'https://louisslutton.com',
    'https://www.louisslutton.com',
    'https://slutton-v2.vercel.app',  # Default Vercel domain
]

# Allow Vercel preview deployments
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://.*\.vercel\.app$",
    r"^https://.*\.railway\.app$",
]

CORS_ALLOW_CREDENTIALS = True

# CSRF trusted origins
CSRF_TRUSTED_ORIGINS = [
    'https://louisslutton.com',
    'https://www.louisslutton.com',
    'https://*.railway.app',
    'https://*.up.railway.app',
    'https://*.vercel.app',
]

# Database
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Static Files with WhiteNoise
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Add WhiteNoise middleware
if 'whitenoise.middleware.WhiteNoiseMiddleware' not in MIDDLEWARE:
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media Files (for user uploads)
if os.environ.get('USE_S3') == 'TRUE':
    # Use S3 for production
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'us-east-1')
else:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Security Headers
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HTTPS
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Channels (WebSockets)
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
        },
    },
}