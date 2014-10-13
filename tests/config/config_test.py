import os
from shuffle.config import config

__current_dir = os.path.dirname(__file__)

config.LOG_FILE = os.path.join(__current_dir, "logging/logging_test.yaml")
config.SHUFFLE_DATA_FILE = os.path.join(__current_dir, "shuffle_data/shuffles_test.json")
config.CLIENT_SECRETS_FILE = os.path.join(__current_dir, "auth/client_secrets.json")

config.EMAIL_TEMPLATES_FOLDER = os.path.join(__current_dir, "shuffle_data/email_templates")

config.GROUPS_BASE_FILE_LOCATION = os.path.join(__current_dir, "tmp/groups")
