LOG_FILE = "logging/logging.yaml"
SHUFFLE_DATA_FILE = "shuffle_data/shuffles.json"
CLIENT_SECRETS_FILE = "auth/client_secrets.json"

CALENDAR_API_VERSION = "v3"
ADMIN_API_VERSION = "directory_v1"
CALENDAR_API_NAME = "calendar"
ADMIN_API_NAME = "admin"

MANDRILL_API_USER = "shuffle-lunch@simplymeasured.com"
MANDRILL_API_KEY = "Nmnt3Dz99JV7XWSF4bWECg"

GROUPS_BASE_FILE_LOCATION = "groups/"

try:
    from config_local import *
except ImportError:
    pass

