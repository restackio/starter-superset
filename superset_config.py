## Mandatory configuration // Do not change

import os
from cachelib.redis import RedisCache


def env(key, default=None):
    return os.getenv(key, default)


CACHE_CONFIG = {
    'CACHE_TYPE': 'redis',
    'CACHE_DEFAULT_TIMEOUT': 300,
    'CACHE_KEY_PREFIX': 'superset_',
    'CACHE_REDIS_HOST': env('REDIS_HOST'),
    'CACHE_REDIS_PORT': env('REDIS_PORT'),
    'CACHE_REDIS_PASSWORD': env('REDIS_PASSWORD'),
    'CACHE_REDIS_DB': env('REDIS_DB', 1),
}
DATA_CACHE_CONFIG = CACHE_CONFIG

SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{env('DB_USER')}:{env('DB_PASS')}@{env('DB_HOST')}:{env('DB_PORT')}/{env('DB_NAME')}"
SQLALCHEMY_TRACK_MODIFICATIONS = True


class CeleryConfig(object):
    CELERY_IMPORTS = ('superset.sql_lab',)
    CELERY_ANNOTATIONS = {'tasks.add': {'rate_limit': '10/s'}}
    BROKER_URL = f"redis://{env('REDIS_HOST')}:{env('REDIS_PORT')}/0"
    CELERY_RESULT_BACKEND = f"redis://{env('REDIS_HOST')}:{env('REDIS_PORT')}/0"


CELERY_CONFIG = CeleryConfig
RESULTS_BACKEND = RedisCache(
    host=env('REDIS_HOST'),
    port=env('REDIS_PORT'),
    key_prefix='superset_results'
)

# This needs to match the name of the environment variable on your application settings on restack console
SECRET_KEY = env('SUPERSET_SECRET_KEY')

# Custom configuration and overrides // Add your configuration below
# https://superset.apache.org/docs/installation/configuring-superset


# Feature flags
# https://superset.apache.org/docs/installation/configuring-superset#feature-flags

FEATURE_FLAGS = {
    "ALERTS_ATTACH_REPORTS": True,
    "ALLOW_ADHOC_SUBQUERY": True,
    "DASHBOARD_CROSS_FILTERS": True,
    "DASHBOARD_RBAC": True,
    "DISABLE_LEGACY_DATASOURCE_EDITOR": True,
    "DRUID_JOINS": True,
    "EMBEDDABLE_CHARTS": True,
    "EMBEDDED_SUPERSET": True,
    "ENABLE_DND_WITH_CLICK_UX": True,
    "ENABLE_EXPLORE_DRAG_AND_DROP": True,
    "ENABLE_TEMPLATE_PROCESSING": True,
    "ENFORCE_DB_ENCRYPTION_UI": True,
    "ESCAPE_MARKDOWN_HTML": True,
    "LISTVIEWS_DEFAULT_CARD_VIEW": True,
    "SCHEDULED_QUERIES": True,
    "SQLLAB_BACKEND_PERSISTENCE": True,
    "SQL_VALIDATORS_BY_ENGINE": True,
    "THUMBNAILS": True,
    "ALERT_REPORTS": True
}

# Data cache config
# https://superset.apache.org/docs/installation/cache/#fallback-metastore-cache

DATA_CACHE_CONFIG = {
    "CACHE_TYPE": "SupersetMetastoreCache",
    "CACHE_KEY_PREFIX": "superset_results",
    "CACHE_DEFAULT_TIMEOUT": 86400,
}

# Superset specific config
ROW_LIMIT = 5000

# Flask-WTF flag for CSRF
WTF_CSRF_ENABLED = True
# Add endpoints that need to be exempt from CSRF protection
# WTF_CSRF_EXEMPT_LIST = ['/api/v1/security/guest_token/']
# A CSRF token that expires in 1 year
WTF_CSRF_TIME_LIMIT = 60 * 60 * 24 * 365

# Set an API key to enable Mapbox visualizations
MAPBOX_API_KEY = env('MAPBOX_API_KEY')

# For allowing anonymous users to see specific Dashboards
# AUTH_ROLE_PUBLIC = "Public"
# PUBLIC_ROLE_LIKE = "Restricted Gamma Public Access"

# To facilitate iFrame embedding of public dashboard
# SESSION_COOKIE_SAMESITE = "None"
# SESSION_COOKIE_SECURE = True
# SESSION_COOKIE_HTTPONLY = True

TALISMAN_ENABLED = False
HTTP_HEADERS = {"X-Frame-Options": "ALLOWALL"}
ENABLE_PROXY_FIX = True

# Enable CORS
ENABLE_CORS = True

# Configure CORS options if necessary (this is optional and can be customized as needed)
CORS_OPTIONS = {
    'supports_credentials': True,
    'allow_headers': ['*'],
    'resources': ['*'],
    'origins': ['*'],  # add the domains you want to enable or keep * to allow all domains.
    # Add other options here as per your requirements
}
