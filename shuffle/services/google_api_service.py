import json
import os

import httplib2
from apiclient import discovery
from oauth2client.client import SignedJwtAssertionCredentials

from shuffle.config import config


class GoogleApiService:
    def __init__(self, authenticate_now=True):
        self.calendar = None
        self.admin = None

        if authenticate_now is False:
            return

        # CLIENT_SECRETS is name of a file containing the OAuth 2.0 information for this
        # application, including client_id and client_secret. You can see the Client ID
        # and Client secret on the APIs page in the Cloud Console:
        # <https://cloud.google.com/console#/project/421792064817/apiui>
        client_secrets_file = open(os.path.join(os.path.dirname(config.__file__), config.CLIENT_SECRETS_FILE))

        client_secrets = json.load(client_secrets_file)
        client_secrets_file.close()

        credentials = SignedJwtAssertionCredentials(client_secrets["client_email"], client_secrets["private_key"], scope=client_secrets["scopes"], sub="cwatts@simplymeasured.com")

        # Create an httplib2.Http object to handle our HTTP requests and authorize it
        # with our good Credentials.
        http = httplib2.Http()
        http = credentials.authorize(http)

        self.set_calendar_api(http)
        self.set_admin_api(http)

    def set_calendar_api(self, http):
        self.calendar = discovery.build(config.CALENDAR_API_NAME, config.CALENDAR_API_VERSION, http=http)

    def set_admin_api(self, http):
        self.admin = discovery.build(config.ADMIN_API_NAME, config.ADMIN_API_VERSION, http=http)
