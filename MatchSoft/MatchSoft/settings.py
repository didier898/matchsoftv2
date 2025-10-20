import os
from pathlib import Path
import dj_database_url

# -------------------
# BASE DIR
# -------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------
# SEGURIDAD / ENTORNO
# -------------------
# Si no existe SECRET_KEY en las variables de entorno, usa esta por defecto (solo para desarrollo)
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-8speg91th%)%#)6bq9n+juhbciqp_l-p7kzu)p0ituee#11#l@"
)

# DEBUG = True en local, False en producción
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# ALLOWED_HOSTS — incluye Render y entorno local
ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS",
    "*.onrender.com,localhost,127.0.0.1,[::1]"
).split(",")

# También aceptamos el dominio de Render dinámico si existe
RENDER_EXTERNAL_HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

print("🟢 ALLOWED_HOSTS:", ALLOWED_HOSTS)  # 👀 solo para depuración, puedes quitarlo luego

# -------------------
# APLICACIONES
# -------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
]

# -------------------
# MIDDLEWARE
# -------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # ✅ necesario para Render (estáticos)
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# -------------------
# URLS Y TEMPLATES
# -------------------
ROOT_URLCONF = "MatchSoft.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # Si usas plantillas globales
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

WSGI_APPLICATION = "MatchSoft.wsgi.application"

# -------------------
# BASE DE DATOS
# -------------------
# En Render, DATABASE_URL se crea automáticamente; en local usa SQLite
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}

# -------------------
# INTERNACIONALIZACIÓN
# -------------------
LANGUAGE_CODE = "es"
TIME_ZONE = "America/Bogota"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# -------------------
# ARCHIVOS ESTÁTICOS (CSS, JS, IMÁGENES)
# -------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# WhiteNoise comprime y cachea los archivos en producción
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# -------------------
# OTRAS CONFIGURACIONES
# -------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Seguridad extra (solo activa si DEBUG=False)
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
