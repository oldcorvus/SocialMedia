
import os
from pathlib import Path

AUTH_USER_MODEL = "useraccounts.CustomUser"

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'SECRET_KEY Not found')


LOGIN_URL = 'account:user_login'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # 3rd-party apps
    'ckeditor_uploader',
    'jalali_date',
    'easy_thumbnails',
    'django_extensions',
    'ckeditor',
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth.registration',
    'django_filters',


    # local apps
    'relations.apps.RelationsConfig',
    'account.apps.AccountConfig',
    'comments.apps.CommentsConfig',
    'bookmark.apps.BookmarkConfig',
    'blog.apps.BlogConfig',
    'core.apps.CoreConfig',
    'api.apps.ApiConfig',
]



# config for django jalali
JALALI_DATE_DEFAULTS = {
    'Strftime': {
        'date': '%y/%m/%d',
        'datetime': '%H:%M:%S _ %y/%m/%d',
    },
    'Static': {
        'js': [
            # loading datepicker
            'admin/js/django_jalali.min.js',
            # OR
            # 'admin/jquery.ui.datepicker.jalali/scripts/jquery.ui.core.js',
            # 'admin/jquery.ui.datepicker.jalali/scripts/calendar.js',
            # 'admin/jquery.ui.datepicker.jalali/scripts/jquery.ui.datepicker-cc.js',
            # 'admin/jquery.ui.datepicker.jalali/scripts/jquery.ui.datepicker-cc-fa.js',
            # 'admin/js/main.js',
        ],
        'css': {
            'all': [
                'admin/jquery.ui.datepicker.jalali/themes/base/jquery-ui.min.css',
            ]
        }
    },
}
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

#config for django rest api
REST_USE_JWT = True
JWT_AUTH_COOKIE = 'moel-auth'
JWT_AUTH_REFRESH_COOKIE = 'moel-token'
REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER':'account.serializers.UserRegisterSeralizer',
    }

REST_AUTH_SERIALIZERS = {
    'LOGIN_SERIALIZER': 'account.serializers.LoginSerializer',
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
                'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
        ],
    'DEFAULT_SEARCH_BACKENDS': [
        'django_filters.rest_framework.DjangoSearchBackend'
        ],
    'DEFAULT_ORDERING_BACKENDS': [
        'django_filters.rest_framework.DjangoOrderingBackend'
        ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100
}

# config for easy thumbnail
THUMBNAIL_ALIASES = {
    '': {
        'post': {'size': (600, 800), 'crop': True},
        'bookmark': {'size': (300, 300), 'crop': True},
        'preview': {'size': (400, 300), 'crop': True},
        'user': {'size': (200, 200), 'crop': True},
        'user-preview': {'size': (100, 100), 'crop': True},
    },
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'socialMedia.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'blog.context_processor.category_navbar',

            ],
        },
    },
]

WSGI_APPLICATION = 'socialMedia.wsgi.application'


# Password validation

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
SITE_ID = 1

# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True



# config for ckeditor
CKEDITOR_UPLOAD_PATH = "ckeditor_uploads/"

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': 600,
    },
}

# Static files (CSS, JavaScript, Images)

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
