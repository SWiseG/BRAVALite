# -*- coding: utf-8 -*-
import os
import sys
from decouple import config
from pathlib import Path
from datetime import timedelta

if os.environ.get("DEBUGPY") == "1":
    import debugpy
    debugpy.listen(("localhost", 5678))
    
# Configurar encoding para UTF-8
if sys.platform.startswith('win'):
    import locale
    locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')
else:
    import locale
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Forçar UTF-8 no Python
import codecs
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================================================================
# CORE SETTINGS
# ==============================================================================

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-ecommerce-admin-change-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1,0.0.0.0', cast=lambda v: [s.strip() for s in v.split(',')])

# ==============================================================================
# APPLICATION DEFINITION
# ==============================================================================

# Django core apps
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Third party apps
THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',
    'django_extensions',
]

# Local apps
LOCAL_APPS = [
    'core',
    'users',
    'products', 
    'orders',
    'customers',
    'dashboard',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# ==============================================================================
# MIDDLEWARE CONFIGURATION
# ==============================================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'core.middleware.DatabaseSchemaMiddleware',  # Schema management
    'core.middleware.AuditMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # I18n support
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'core.middleware.UserLanguageMiddleware',  # Custom language
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'brava.urls'

# ==============================================================================
# TEMPLATE CONFIGURATION
# ==============================================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'web',  # SPA templates
            BASE_DIR / 'templates',  # Django templates
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',  # I18n context
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.global_settings',  # Custom context
            ],
        },
    },
]

WSGI_APPLICATION = 'brava.wsgi.application'

# ==============================================================================
# DATABASE CONFIGURATION (Multi-Schema PostgreSQL)
# ==============================================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='brava_lite'),
        'USER': config('DB_USER', default='brava'),
        'PASSWORD': config('DB_PASSWORD', default='BRV2025DevOps'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
        'OPTIONS': {
            'options': '-c search_path=BRAVA,public',  # Schema padrão
        },
        'CONN_MAX_AGE': 60,
        'ATOMIC_REQUESTS': True,
    }
}


# Database routing for multi-schema
DATABASE_ROUTERS = ['core.database.manager.BRAVAManager']

# ==============================================================================
# DJANGO REST FRAMEWORK CONFIGURATION
# ==============================================================================

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'JSON_ENCODER': 'brava.settings.UUIDEncoder',
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour'
    },
    'EXCEPTION_HANDLER': 'core.exceptions.custom_exception_handler',
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}

# ==============================================================================
# JWT CONFIGURATION
# ==============================================================================

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=24),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,
    
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
    
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',
    
    'JTI_CLAIM': 'jti',
    
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# ==============================================================================
# CORS CONFIGURATION
# ==============================================================================

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:3000",  # Para desenvolvimento frontend separado
    "http://127.0.0.1:3000",
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'cache-control',
]

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# ==============================================================================
# CUSTOM USER MODEL
# ==============================================================================

AUTH_USER_MODEL = 'users.User'

# ==============================================================================
# AUTHENTICATION & AUTHORIZATION
# ==============================================================================

LOGIN_URL = '/auth/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Session configuration
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 86400  # 24 horas
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# CSRF configuration
CSRF_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_USE_SESSIONS = True

# ==============================================================================
# INTERNATIONALIZATION (I18N)
# ==============================================================================

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Supported languages
LANGUAGES = [
    ('pt-br', 'Português Brasil'),
    ('en-us', 'English (US)'),
]

# Translation files
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# ==============================================================================
# STATIC FILES CONFIGURATION
# ==============================================================================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

os.makedirs(BASE_DIR / 'web', exist_ok=True)
os.makedirs(BASE_DIR / 'static', exist_ok=True)
os.makedirs(BASE_DIR / 'media', exist_ok=True)
os.makedirs(BASE_DIR / 'logs', exist_ok=True)

STATICFILES_DIRS = [
    BASE_DIR / 'web',  # SPA assets
    BASE_DIR / 'static',  # Additional static files
]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# ==============================================================================
# MEDIA FILES CONFIGURATION
# ==============================================================================

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# File upload settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000

# ==============================================================================
# EMAIL CONFIGURATION
# ==============================================================================

# Para desenvolvimento
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = config('EMAIL_HOST', default='localhost')
    EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
    EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
    EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')

DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@ecommerce-admin.com')
SERVER_EMAIL = config('SERVER_EMAIL', default='admin@ecommerce-admin.com')

# ==============================================================================
# CACHE CONFIGURATION
# ==============================================================================

if DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': config('REDIS_URL', default='redis://127.0.0.1:6379/1'),
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            },
            'KEY_PREFIX': 'brava',
            'TIMEOUT': 300,  # 5 minutos
        }
    }

# Cache time for different types of data
CACHE_TTL = {
    'SHORT': 300,      # 5 minutos
    'MEDIUM': 1800,    # 30 minutos  
    'LONG': 3600,      # 1 hora
    'VERY_LONG': 86400 # 24 horas
}

# ==============================================================================
# LOGGING CONFIGURATION
# ==============================================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'formatter': 'verbose',
        },
        'db_file': {
            'level': 'DEBUG' if DEBUG else 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'db_queries.log',
            'formatter': 'verbose',
        },
        'api_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'api.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['db_file'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
        'rest_framework': {
            'handlers': ['api_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'brava': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
    },
}

# Criar diretório de logs se não existir
import os
os.makedirs(BASE_DIR / 'logs', exist_ok=True)

# ==============================================================================
# SECURITY SETTINGS
# ==============================================================================

if not DEBUG:
    # HTTPS settings
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    
    # Security headers
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = 31536000  # 1 ano
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Cookie security
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # Referrer policy
    SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# Allowed file extensions for uploads
ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
ALLOWED_DOCUMENT_EXTENSIONS = ['.pdf', '.doc', '.docx', '.xls', '.xlsx']

# Maximum file sizes (in bytes)
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB
MAX_DOCUMENT_SIZE = 10 * 1024 * 1024  # 10MB

# ==============================================================================
# DJANGO EXTENSIONS CONFIGURATION
# ==============================================================================

if DEBUG:
    SHELL_PLUS_PRINT_SQL = True
    SHELL_PLUS_PRINT_SQL_TRUNCATE = 1000

# ==============================================================================
# CUSTOM SETTINGS
# ==============================================================================

# Application specific settings
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
import uuid
import json
class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            return str(obj)
        return super().default(obj)

# API versioning
API_VERSION = 'v1'

# Pagination settings
REST_FRAMEWORK_PAGE_SIZE = 20
REST_FRAMEWORK_MAX_PAGE_SIZE = 100

# Business settings
BUSINESS_SETTINGS = {
    'COMPANY_NAME': config('COMPANY_NAME', default='BRAVA'),
    'COMPANY_EMAIL': config('COMPANY_EMAIL', default='noreplybravass@gmail.com'),
    'SUPPORT_EMAIL': config('SUPPORT_EMAIL', default='bravassolutions@gmail.com'),
    'DEFAULT_CURRENCY': 'BRL',
    'DEFAULT_LANGUAGE': 'pt-br',
    'TIMEZONE': 'America/Sao_Paulo',
}

# Integration settings
INTEGRATION_SETTINGS = {
    'PAGSEGURO': {
        'SANDBOX': config('PAGSEGURO_SANDBOX', default=True, cast=bool),
        'APP_ID': config('PAGSEGURO_APP_ID', default=''),
        'APP_KEY': config('PAGSEGURO_APP_KEY', default=''),
    },
    'MERCADOLIVRE': {
        'CLIENT_ID': config('ML_CLIENT_ID', default=''),
        'CLIENT_SECRET': config('ML_CLIENT_SECRET', default=''),
    },
    'FACEBOOK': {
        'APP_ID': config('FB_APP_ID', default=''),
        'APP_SECRET': config('FB_APP_SECRET', default=''),
    },
    'SHOPEE': {
        'PARTNER_ID': config('SHOPEE_PARTNER_ID', default=''),
        'PARTNER_KEY': config('SHOPEE_PARTNER_KEY', default=''),
    }
}

# File storage settings
if not DEBUG:
    # Configuração para storage em produção (AWS S3, etc.)
    pass

# ==============================================================================
# DEVELOPMENT SETTINGS
# ==============================================================================

if DEBUG:
    # Debug toolbar (opcional)
    try:
        import debug_toolbar
        INSTALLED_APPS += ['debug_toolbar']
        MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
        INTERNAL_IPS = ['127.0.0.1', 'localhost']
        
        DEBUG_TOOLBAR_CONFIG = {
            'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG,
        }
    except ImportError:
        pass
    
    # Permitir todos os hosts em desenvolvimento
    ALLOWED_HOSTS = ['*']

# ==============================================================================
# ENVIRONMENT SPECIFIC IMPORTS
# ==============================================================================

# ==============================================================================
# FINAL VALIDATIONS
# ==============================================================================

import sys

# Validar configurações obrigatórias
if not DEBUG:
    required_settings = [
        'DB_PASSWORD',
        'EMAIL_HOST_USER', 
        'EMAIL_HOST_PASSWORD',
    ]
    
    for setting in required_settings:
        if not config(setting, default=None):
            raise ValueError(f'Setting {setting} is required in production')

# Exibir informações de configuração em desenvolvimento
if DEBUG and 'runserver' in sys.argv:
    print("BRAVA Lite - DEV")
    print(f"Database: {DATABASES['default']['NAME']} @ {DATABASES['default']['HOST']}")
    print(f"Language: {LANGUAGE_CODE} | Timezone: {TIME_ZONE}")
    print(f"JWT Lifetime: {SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']}")
    print(f"Media: {MEDIA_ROOT}")
    print(f"Static: {STATIC_ROOT}")
    print("="*60)
