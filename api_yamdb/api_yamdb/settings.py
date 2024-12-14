import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()


#  /home/../YaMDb/api_yamdb
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.getenv("SECRET_KEY", default="default")

DEBUG = bool(os.getenv("DEBUG", False))

ALLOWED_HOSTS = ["127.0.0.1"]


INSTALLED_APPS = [
    "debug_toolbar",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "api.apps.ApiConfig",
    "users.apps.UsersConfig",
    "rest_framework_simplejwt",
    "rest_framework",
    "django_filters",
    "reviews.apps.ReviewsConfig",
    # documentation
    "drf_spectacular",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "api_yamdb.urls"

TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATES_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "api_yamdb.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": os.getenv(
            "DB_ENGINE", default="django.db.backends.postgresql"
        ),
        "NAME": os.getenv("DB_NAME", default="postgres"),
        "USER": os.getenv("POSTGRES_USER", default="postgres"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", default="postgres"),
        "HOST": os.getenv("DB_HOST", default="localhost"),
        "PORT": os.getenv("DB_PORT", default="5432"),
    }
}

# При локальном тестирование
if os.getenv("DB") == "sqlite":
    DATABASES["default"] = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "ru"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTH_USER_MODEL = "users.User"

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

STATIC_URL = "/static/"
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
STATIC_ROOT = os.path.join(BASE_DIR, "collectstatic")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 5,
    "DATETIME_FORMAT": "%Y-%m-%dT%H:%M:%SZ",
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# Аутентификация Для тестирования SQL-запросов в debug_toolbar через браузер
# REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"].extend(
#     [
#         "rest_framework.authentication.BasicAuthentication",
#         "rest_framework.authentication.SessionAuthentication",
#     ]
# )

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),  # Время жизни токена 1 день
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(days=1),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}

# По умолчанию email будет выводиться в консоль
EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend"
)
# Эти настройки необходимы, если определить SMTP backend
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True


# Celery settings with Redis
CELERY_BROKER_URL = os.getenv("REDIS_SERVER")
CELERY_RESULT_BACKEND = os.getenv("REDIS_SERVER")


# Cache settings with Redis
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": os.getenv("REDIS_SERVER"),
    }
}

# Ключ кеша для кода верификации
CACHE_KEY_CONFIRM_CODE = "confirmation_code"
# Время хранения кеша для кода верификации в секундах
CACHE_TIMEOUT = 300

INTERNAL_IPS = ["127.0.0.1"]


# Настройки документации DRF Spectacular
DESCRIPTION_DOC = """
# Описание
Проект **YaMDb** собирает отзывы пользователей на различные произведения.
# Алгоритм регистрации и аутентификации пользователей
1. Пользователь отправляет POST-запрос с указанием своего `email`
на эндпоинт `/api/v1/auth/send_confirm_code/`.
2. **YaMDB** отправляет письмо с кодом подтверждения (`confirmation_code`)
на адрес  `email`.
3. Пользователь отправляет POST-запрос с параметрами `email` и
`confirmation_code` на эндпоинт `/api/v1/auth/token/`, в ответе на запрос ему
приходит `token` (JWT-токен). Если пользователь ещё не зарегистрирован, то он
автоматически сохраняется в БД.
4. При желании пользователь отправляет PATCH-запрос на эндпоинт
`/api/v1/users/me/` и заполняет поля в своём профайле
(описание полей — в документации).
# Пользовательские роли
- **Аноним** — может просматривать описания произведений,
читать отзывы и комментарии.
- **Аутентифицированный пользователь** (`user`) — может, как и **Аноним**,
читать всё, дополнительно он может публиковать отзывы и ставить оценку
произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы;
может редактировать и удалять **свои** отзывы и комментарии.
Эта роль присваивается по умолчанию каждому новому пользователю.
- **Модератор** (`moderator`) — те же права, что и у
**Аутентифицированного пользователя** плюс право удалять **любые** отзывы
и комментарии.
- **Администратор** (`admin`) — полные права на управление
всем контентом проекта. Может создавать и удалять произведения,
категории и жанры. Может назначать роли пользователям.
- **Суперюзер Django** — обладает правами администратора (`admin`)
"""


SPECTACULAR_SETTINGS = {
    "TITLE": "YaMDb API",
    "DESCRIPTION": DESCRIPTION_DOC,
    "VERSION": "2.0.0",
    "CONTACT": {
        "name": "Биссалиев Олег",
        "url": "https://github.com/bissaliev",
        "email": "bissaliev21@gmail.com",
    },
    "SWAGGER_UI_SETTINGS": {
        "docExpansion": "none",  # Настройка поведения Swagger UI
        "defaultModelsExpandDepth": -1,  # Скрыть примеры моделей
    },
}
