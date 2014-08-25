import sys

from shuffle.config import config
from shuffle.services.google_api_service import GoogleApiService
from shuffle.services.shuffle_service import ShuffleService


def main(argv):
    # Parse the command-line flags.
    is_dev_environment = False
    for i in range(len(argv)):
        if argv[i] == "--env":
            if argv[i + 1] == "dev":
                is_dev_environment = True

    shuffle_service = ShuffleService(config.SHUFFLE_DATA_FILE, GoogleApiService())
    shuffle_service.execute(is_dev_environment)

if __name__ == '__main__':
    main(sys.argv)
