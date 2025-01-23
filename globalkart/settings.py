"""
Django settings for globalkart project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
from django.contrib.messages import constants as messages

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'n^#*)$e-1#z+#ypnzq0!+n&!ww5*n7@bmvxw4%=9leco5pbbb@'

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
    'category',  # Custom app for managing categories
    'accounts',  # Custom app for user accounts
    'store',     # Custom app for the store
    'carts',     # Custom app for shopping carts
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Provides security enhancements
    'django.contrib.sessions.middleware.SessionMiddleware',  # Manages session data
    'django.middleware.common.CommonMiddleware',  # Adds standard HTTP headers
    'django.middleware.csrf.CsrfViewMiddleware',  # Protects against Cross-Site Request Forgery
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Handles user authentication
    'django.contrib.messages.middleware.MessageMiddleware',  # Enables messages framework
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Prevents clickjacking
]

ROOT_URLCONF = 'globalkart.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],  # Directory for custom templates
        'APP_DIRS': True,  # Looks for templates in installed apps
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',  # Adds debugging context
                'django.template.context_processors.request',  # Adds request context
                'django.contrib.auth.context_processors.auth',  # Adds auth context
                'django.contrib.messages.context_processors.messages',  # Adds message context
                'category.context_processors.menu_links',  # Custom context processor for menu links
                'carts.context_processors.counter',  # Custom context processor for cart counter
            ],
        },
    },
]

WSGI_APPLICATION = 'globalkart.wsgi.application'

# Custom user model configuration
AUTH_USER_MODEL = 'accounts.Account'  # Custom user model for accounts


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Using SQLite for development
        'NAME': BASE_DIR / 'db.sqlite3',  # Database file path
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # Validates password similarity
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # Enforces minimum password length
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # Prevents common passwords
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # Prevents fully numeric passwords
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/
LANGUAGE_CODE = 'en-us'  # Default language
TIME_ZONE = 'UTC'  # Default timezone
USE_I18N = True  # Enable internationalization
USE_L10N = True  # Enable localization
USE_TZ = True  # Enable timezone support

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_URL = '/static/'  # URL for serving static files
STATIC_ROOT = BASE_DIR / 'static'  # Directory where static files are collected
STATICFILES_DIRS = [
    BASE_DIR / 'globalkart/static',  # Additional directories for static files
]

# Media files configuration
MEDIA_URL = '/media/'  # URL for serving media files
MEDIA_ROOT = BASE_DIR / 'media'  # Directory where media files are stored

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'  # Default for new models

# Message tags for the messages framework
MESSAGE_TAGS = {
    messages.ERROR: "danger",  # Maps error messages to "danger" Bootstrap class
}

# Static files storage configuration
# Updated for Django 4.2+ to use manifest storage
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'



# Configuting the SMTP connection
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_HOST ='smtp.gmail.com'
# EMAIL_PORT = 587 #this is  Port number for GMAIL, it will be different for other platforms
# EMAIL_HOST_USER = 'esaipradeep4@gmail.com'
# EMAIL_HOST_PASSWORD = ''
# EMAIL_USE_TLS = True
# EMAIL_USE_SSL = False
# DEFAULT_FROM_EMAIL = 'esaipradeep4@gmail.com'