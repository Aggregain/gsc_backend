import os
from datetime import timedelta
from os.path import join
from pathlib import Path

from dotenv import load_dotenv


def get_bool_env(var_name, default=False):
    value = os.getenv(var_name, str(default)).lower()
    return value in ("1", "true", "yes", "on")


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'secret_key')

DEBUG = get_bool_env('DEBUG', True)

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'unfold',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'storages',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'drf_spectacular',
    'django_celery_results',
    'django_celery_beat',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'dj_rest_auth.registration',
    'ckeditor',
    'debug_toolbar',

    'accounts.apps.AccountsConfig',
    'common.apps.CommonConfig',
    'applications.apps.ApplicationsConfig',
    'wishlist.apps.WishlistConfig',
    'notifications.apps.NotificationsConfig',
]

INTERNAL_IPS = [
    # ...
    '127.0.0.1',
]
# REST_AUTH = {
#     'TOKEN_MODEL': None,
#     'USE_JWT': True,
# }

SITE_ID = 1
# ACCOUNT_USER_MODEL_USERNAME_FIELD = None
# ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']
# ACCOUNT_LOGIN_METHODS = {'email'}
# SOCIALACCOUNT_EMAIL_AUTHENTICATION = True
# SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True
# PASSWORD_RESET_USE_SITES_DOMAIN = True

# BACKEND_BASE_URL = os.getenv('BACKEND_BASE_URL')
# GOOGLE_OAUTH_CALLBACK_PATH = os.getenv('GOOGLE_OAUTH_CALLBACK_PATH')
# GOOGLE_OAUTH_CALLBACK_URL = BACKEND_BASE_URL + GOOGLE_OAUTH_CALLBACK_PATH
#
# GOOGLE_SECRET_KEY = os.getenv('GOOGLE_SECRET_KEY')
# GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('EMAIL_HOST_USER')

# SOCIALACCOUNT_PROVIDERS = {
#     'google': {
#         'APP': {
#             'client_id': GOOGLE_CLIENT_ID,
#             'secret': GOOGLE_SECRET_KEY,
#             'key': ''
#         },
#         'SCOPE': [
#             'profile',
#             'email',
#         ],
#         'AUTH_PARAMS': {
#             'access_type': 'online',
#         }
#     }
# }

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',

]

if DEBUG:
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
ROOT_URLCONF = 'gsc_backend.urls'


DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: True,
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'gsc_backend.wsgi.application'

IN_DOCKER = get_bool_env('IN_DOCKER', True)

DATABASES = {}
postgres = {
    'ENGINE': 'django.db.backends.postgresql',
    'HOST': os.getenv('DB_HOST'),
    'NAME': os.getenv('DB_NAME'),
    'USER': os.getenv('DB_USER'),
    'PASSWORD': os.getenv('DB_PASS')
}

sqlite = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'db.sqlite3',
}

FORCE_SCRIPT_NAME = "/api"

CSRF_TRUSTED_ORIGINS = [
    "https://gsc.kz",
    "https://*.gsc.kz",
]
if IN_DOCKER:
    DATABASES['default'] = postgres

    AWS_ACCESS_KEY_ID = os.getenv('MINIO_ROOT_USER')
    AWS_SECRET_ACCESS_KEY = os.getenv('MINIO_ROOT_PASSWORD')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')

    AWS_S3_ENDPOINT_URL = os.getenv('AWS_S3_ENDPOINT_URL')
    AWS_S3_USE_SSL = False
    AWS_S3_FILE_OVERWRITE = True
    AWS_DEFAULT_ACL = None
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_CUSTOM_DOMAIN = f'{os.getenv('AWS_S3_CUSTOM_DOMAIN')}/{AWS_STORAGE_BUCKET_NAME}'
    AWS_S3_URL_PROTOCOL = 'https:'

    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3.S3Storage",
            "OPTIONS": {
                "bucket_name": AWS_STORAGE_BUCKET_NAME,
                "location": "media",
                "custom_domain": AWS_S3_CUSTOM_DOMAIN,
                "addressing_style": "path"
            },
        },
        "staticfiles": {
            "BACKEND": "storages.backends.s3.S3Storage",
            "OPTIONS": {
                "bucket_name": AWS_STORAGE_BUCKET_NAME,
                "location": "static",
                "custom_domain": AWS_S3_CUSTOM_DOMAIN,
                "addressing_style": "path"
            },
        },
    }
else:
    DATABASES['default'] = sqlite
    STATIC_URL = 'static/'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Asia/Aqtobe'

USE_I18N = True

USE_TZ = True

AUTH_USER_MODEL = 'accounts.Account'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',
                                'rest_framework.filters.OrderingFilter',),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DATE_FORMAT': "%d/%m/%Y",
    'DATE_INPUT_FORMATS': ["%d/%m/%Y"],
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),


}

SPECTACULAR_SETTINGS = {

    'SWAGGER_UI_SETTINGS': {
        'persistAuthorization': True,
    },
    'COMPONENT_SPLIT_REQUEST': True

}
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=6),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=2),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

CELERY_URL = os.getenv('CELERY_BROKER_URL')
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f'{CELERY_URL}/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    }
}

CELERY_BROKER_URL = f'{CELERY_URL}/0'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_TIMEZONE = 'Asia/Aqtobe'

CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

UNFOLD = {
    "SITE_TITLE": "Админ панель GSC STUDY",
    "SITE_HEADER": "Управление данными сайта",
    "THEME": "dark",
}


#TODO
# google login
# reset password



