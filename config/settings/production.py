"""
Production settings for Aura Link.
"""

from .base import *
from decouple import config
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
import dj_database_url
import os

# Security
DEBUG = False

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*').split(',')

# HTTPS and Security Headers
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# CORS (restrict to specific origins in production)
CORS_ALLOW_ALL_ORIGINS = config('CORS_ALLOW_ALL_ORIGINS', default=False, cast=bool)
if not CORS_ALLOW_ALL_ORIGINS:
    CORS_ALLOWED_ORIGINS = config('CORS_ORIGINS', default='').split(',')
CORS_ALLOW_CREDENTIALS = True

# Database
# Render provides a DATABASE_URL environment variable
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# WhiteNoise for static files
# Middleware should be right after SecurityMiddleware
if 'whitenoise.middleware.WhiteNoiseMiddleware' not in MIDDLEWARE:
    # Index 1 is after SecurityMiddleware in base.py
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# Static and Media files
if STORAGE_TYPE == 's3':
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'
else:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Sentry Error Tracking
SENTRY_DSN = config('SENTRY_DSN', default='')
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.1,
        send_default_pii=True,
        environment='production',
    )

# Logging (JSON format for production, console only)
LOGGING['handlers']['console']['formatter'] = 'json'
# Remove file handler as Render filesystem is ephemeral and can't be relied upon for logs
if 'file' in LOGGING['handlers']:
    LOGGING['handlers'].pop('file')
if 'file' in LOGGING['root']['handlers']:
    LOGGING['root']['handlers'].remove('file')
for logger in LOGGING['loggers'].values():
    if 'file' in logger['handlers']:
        logger['handlers'].remove('file')

LOGGING['root']['level'] = 'INFO'

# Caching (more aggressive in production)
CACHES['default']['OPTIONS']['SOCKET_CONNECT_TIMEOUT'] = 5
CACHES['default']['OPTIONS']['SOCKET_TIMEOUT'] = 5

# Email backend (real SMTP in production)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
