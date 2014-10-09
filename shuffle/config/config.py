import os

__current_dir = os.path.dirname(__file__)

LOG_FILE = os.path.join(__current_dir, "logging/logging.yaml")
SHUFFLE_DATA_FILE = os.path.join(__current_dir, "shuffle_data/shuffles.json")
CLIENT_SECRETS_FILE = os.path.join(__current_dir, "auth/client_secrets.json")

EMAIL_TEMPLATES_FOLDER = os.path.join(__current_dir, "shuffle_data/email_templates")

CALENDAR_API_VERSION = "v3"
ADMIN_API_VERSION = "directory_v1"
CALENDAR_API_NAME = "calendar"
ADMIN_API_NAME = "admin"

MANDRILL_API_USER = "shuffle-lunch@simplymeasured.com"
MANDRILL_API_KEY = "Nmnt3Dz99JV7XWSF4bWECg"

GROUPS_BASE_FILE_LOCATION = os.path.join(__current_dir, "groups")

try:
    from tests.config.config_test import *
except ImportError:
    pass
