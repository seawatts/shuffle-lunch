import os
from shuffle.config import config
from shuffle.config.logging.setup_logging import setup_logging

setup_logging(os.path.join(os.path.dirname(config.__file__), config.LOG_FILE))