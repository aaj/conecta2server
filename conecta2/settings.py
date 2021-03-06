"""
Django settings for conecta2 project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

ADMINS = (
    ('Armando Alvarado', 'mando.alvarado.jose@gmail.com'),
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%r$4ot4%pa(e_zum#509hl06h0ykhc+%w0809d&c5$_1t&^%$b'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    'meapuntohonduras.com',
    'www.meapuntohonduras.com'
]


# Application definition

INSTALLED_APPS = (
    'djangocms_admin_style',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'inicio',
    'eventos',
    'instituciones',
    'noticias',
    'votos',
    'usuarios',
    'social.apps.django_app.default',
    'geoposition',
    'easy_thumbnails',
    'easy_timezones',
    'tokenapi',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'easy_timezones.middleware.EasyTimezoneMiddleware',
    'conecta2.middleware.PlatformIdentificationMiddleware',
)

ROOT_URLCONF = 'conecta2.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates/')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'conecta2.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'conecta2',
        'USER': 'conecta2_admin',
        'PASSWORD': 'admin',
        'HOST': '',
        'PORT': '',
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'es-hn'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/



AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    'tokenapi.backends.TokenBackend',
)

SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['email']
SOCIAL_AUTH_FACEBOOK_KEY = '1190381087643213'
SOCIAL_AUTH_FACEBOOK_SECRET = '277892e5cdf6deef2d2541c60188e422'

SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'gender', 'bio', 'birthday']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id,name,email,gender,bio,birthday', # needed starting from protocol v2.4
}


SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.social_auth.associate_by_email',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    #'social.pipeline.user.user_details'
    'usuarios.pipeline.user_details',
)

MEDIA_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), '../../media/').replace('\\','/'))
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), '../../static/').replace('\\','/'))
STATIC_URL = '/static/'

THUMBNAIL_PRESERVE_EXTENSIONS = True
THUMBNAIL_ALIASES = {
    '': {
        'small': {'size': (32, 32), 'crop': 'smart'},
        'medium': {'size': (256, 256), 'crop': 'smart'},
        'large': {'size': (512, 512), 'crop': 'smart'}
    },
}

LOGIN_URL = '/usuarios/login'

GEOIP_DATABASE = os.path.join(BASE_DIR, 'GeoLiteCity.dat')

TOKEN_CHECK_ACTIVE_USER = True

DATETIME_INPUT_FORMATS = ('%Y-%m-%dT%H:%M:%S%z',)

EMAIL_HOST = 'smtp.webfaction.com'
EMAIL_HOST_USER = 'info_meapunto'
EMAIL_HOST_PASSWORD = '1nf0_meapunto'
DEFAULT_FROM_EMAIL = 'Info MeApunto <info@meapuntohonduras.com>'
SERVER_EMAIL = 'info@meapuntohonduras.com'

try:
    from local_settings import *
except ImportError:
    pass