import os

__current_dir = os.path.dirname(__file__)

LOG_FILE = os.path.join(__current_dir, "logging/logging_test.yaml")
SHUFFLE_DATA_FILE = os.path.join(__current_dir, "shuffle_data/shuffles_test.json")
CLIENT_SECRETS_FILE = os.path.join(__current_dir, "auth/client_secrets.json")

EMAIL_TEMPLATES_FOLDER = os.path.join(__current_dir, "shuffle_data/email_templates")

GROUPS_BASE_FILE_LOCATION = os.path.join(__current_dir, "tmp/groups")

