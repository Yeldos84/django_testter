"""
Django settings for testter project.

Generated by 'django-admin startproject' using Django 3.2.25.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os.path
from pathlib import Path



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-pq6yp(%-1-q5rl#sov!h&5t82=4)*^ahisu5qo*4obilv=bhu-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'social_django',
    'rest_framework',
    'corsheaders',

    'testapp'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',


]

ROOT_URLCONF = 'testter.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'testter.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "ru-ru"

TIME_ZONE = 'Asia/Almaty'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
# For Upload File
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'eldos.dos@gmail.com'
EMAIL_HOST_PASSWORD = 'gdra uuwx dury unus'

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER
EMAIL_ADMIN = EMAIL_HOST_USER


AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.google.GoogleOAuth',
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.google.GooglePlusAuth',
)


SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '1033274941074-gpj8u7n5f76999ku4urhiul398mjschs.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'

LOGIN_URL = '/social-auth/login/google-oauth2/'

SOCIAL_AUTH_URL_NAMESPACE = 'social'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = 'http://127.0.0.1:8081/complete/google-oauth2/'


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

#Logs

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': True,
#     'filters': {
#         'require_debug_false': {
#             '()': 'django.utils.log.RequireDebugFalse',
#         },
#         'require_debug_true': {
#             '()': 'django.utils.log.RequireDebugTrue',
#         },
#     },
#     'formatters': {
#         'simple': {
#             'format': '[%(asctime)s] %(levelname)s: %(message)s',
#             'datefmt': '%Y.%m.%d %H:%M:%S',
#         },
#     },
#     'handlers': {
#         'console_dev': {
#             'class': 'logging.StreamHandler',
#             'formatter': 'simple',
#             'filters': ['require_debug_true'],
#         },
#         'console_prod': {
#             'class': 'logging.StreamHandler',
#             'formatter': 'simple',
#             'level': 'ERROR',
#             'filters': ['require_debug_false'],
#         },
#         'file': {
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': 'C:/dlog/django-site.log',
#             'maxBytes': 1048576,
#             'backupCount': 10,
#             'formatter': 'simple',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console_dev', 'console_prod'],
#         },
#         'django.server': {
#             'handlers': ['file'],
#             'level': 'INFO',
#             'propagate': True,
#         },
#     }
# }


