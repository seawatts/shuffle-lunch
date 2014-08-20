import argparse
import sys

from oauth2client import tools

from shuffle.config import config
from shuffle.services.google_api_service import GoogleApiService
from shuffle.services.shuffle_service import ShuffleService

def main(argv):
    # Parse the command-line flags.
    shuffle_service = ShuffleService(config.SHUFFLE_DATA_FILE, GoogleApiService())
    shuffle_service.execute()

if __name__ == '__main__':
    main(sys.argv)
