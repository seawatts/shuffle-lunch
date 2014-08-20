LOG_FILE = "logging/logging.yaml"
SHUFFLE_DATA_FILE = "shuffle_data/shuffles.json"
CLIENT_SECRETS_FILE = "auth/client_secrets.json"

CALENDER_API_VERSION = "v3"
GMAIL_API_VERSION = "v1"
ADMIN_API_VERSION = "directory_v1"
CALENDER_API_NAME = "calendar"
GMAIL_API_NAME = "gmail"
ADMIN_API_NAME = "admin"

try:
    from config_local import *
except ImportError:
    pass

try:
    from config_test import *
except ImportError:
    pass

