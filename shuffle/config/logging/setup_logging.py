from logging import getLogger, getLevelName
import os
import logging.config

import yaml


def setup_logging(default_path='logging.yaml', default_level=logging.INFO):
    """Setup logging configuration """
    path = default_path

    if os.path.exists(path):
        try:
            with open(path, 'rt') as f:
                config = yaml.load(f.read())
            logging.config.dictConfig(config)
        except IOError as error:
            logging.error("Could not read logging file. This is unrecoverable, please create a logging file and try again. %s" % error)
            return
    else:
        logging.basicConfig(level=default_level)
    logging.info("Logging level: " + getLevelName(getLogger().getEffectiveLevel()))