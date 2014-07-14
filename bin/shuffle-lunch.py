# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Command-line skeleton application for Calendar API.
Usage:
  $ python sample.py

You can also get help on all the command-line flags the program understands
by running:

  $ python sample.py --help

"""

import argparse
import base64
from datetime import datetime
from email import errors
from email.mime.text import MIMEText
import httplib2
import os
import sys

from apiclient import discovery
from oauth2client import file
from oauth2client import client
from oauth2client import tools

# Parser for command-line arguments.
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[tools.argparser])


# CLIENT_SECRETS is name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret. You can see the Client ID
# and Client secret on the APIs page in the Cloud Console:
# <https://cloud.google.com/console#/project/421792064817/apiui>
CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')

# Set up a Flow object to be used for authentication.
# Add one or more of the following scopes. PLEASE ONLY ADD THE SCOPES YOU
# NEED. For more information on using scopes please see
# <https://developers.google.com/+/best-practices>.
FLOW = client.flow_from_clientsecrets(CLIENT_SECRETS,
  scope=[
      'https://www.googleapis.com/auth/calendar',
      'https://www.googleapis.com/auth/calendar.readonly',
      'https://www.googleapis.com/auth/admin.directory.group.member.readonly',
      'https://www.googleapis.com/auth/gmail.compose',
  ],
    message=tools.message_if_missing(CLIENT_SECRETS))

DOMAIN = 'simplymeasured.com'
EMAIL_FROM_NAME = "Shuffle Lunch"
EMAIL_FROM = 'shuffle-lunch@' + DOMAIN
EMAIL_SUBJECT = 'Your shuffle lunch team'
RECURRING_EVENT_ID = 'nn06htjcggc2g55fktqmivssf8'
ALL_GROUP_ALIAS = 'all@' + DOMAIN

def main(argv):
  # Parse the command-line flags.
  flags = parser.parse_args(argv[1:])

  # If the credentials don't exist or are invalid run through the native client
  # flow. The Storage object will ensure that if successful the good
  # credentials will get written back to the file.
  storage = file.Storage('credentials.dat')
  credentials = storage.get()
  if credentials is None or credentials.invalid:
    credentials = tools.run_flow(FLOW, storage, flags)

  # Create an httplib2.Http object to handle our HTTP requests and authorize it
  # with our good Credentials.
  http = httplib2.Http()
  http = credentials.authorize(http)

  # Construct the service object for the interacting with the Calendar API.
  calendar = discovery.build('calendar', 'v3', http=http)
  gmail = discovery.build('gmail', 'v1', http=http)
  admin = discovery.build('admin', 'directory_v1', http=http)

  try:
    print "Success! Now add code here."
    # allAccepted = GetAllAcceptedAttendees(calendar, admin)
    # randomizedGroups = CreateRandomizeGroups(allAccepted)
    randomizedGroups = []
    randomizedGroups.append(['cwatts@simplymeasured.com'])
    SendEmailsToGroups(gmail, randomizedGroups)

  except client.AccessTokenRefreshError:
    print ("The credentials have been revoked or expired, please re-run"
      "the application to re-authorize")


def GetAllAcceptedAttendees(calendar, admin):
    allAccepted = []
    emails = admin.members().list(groupKey=ALL_GROUP_ALIAS).execute()

    # TOOD: Loop through all the emails in the 'all' alias and get each event to see if they have accepted
    for usersEmail in emails:
        # print email['email']
        # usersEmail = "cwatts@" + DOMAIN
        eventId = ComposeEventId()
        event = calendar.events().get(calendarId=usersEmail, eventId=eventId).execute()
        attendees = event['attendees']
        accepted = GetAcceptedAttendees(attendees)
        allAccepted.append(accepted)

    return allAccepted


def ComposeEventId():
    currentDate = datetime.utcnow().strftime("%Y%m%dT190000Z")
    return RECURRING_EVENT_ID + "_" + currentDate


def GetAcceptedAttendees(attendees):
    accepted = []
    declined = []
    needsAction = []
    # TODO: Figure out how to see which user we should get
    usersEmail = "cwatts@" + DOMAIN

    for attendee in attendees:
        if attendee['email'] == usersEmail:
            responseStatus = attendee['responseStatus']
            if responseStatus == 'accepted':
                accepted.append(attendee)
            elif responseStatus == 'declined':
                declined.append(attendee)
            elif responseStatus == 'needsAction':
                needsAction.append(attendee)

            continue

    print 'accepted {}'.format(len(accepted))
    print 'needsAction {}'.format(len(needsAction))
    print 'declined {}'.format(len(declined))

    return accepted


def CreateRandomizeGroups(users):
    groups = []
    # TODO: Create random algoirthm here
    # for user in users:

    return groups


def SendEmailsToGroups(gmail, randomizedGroups):
    for group in randomizedGroups:
        # TODO: Combine emails into one email
        for user in group:
            email_to = user
            message = CreateMessage(EMAIL_FROM, email_to, EMAIL_SUBJECT, "hello")
            SendMessage(gmail, 'me', message)


def CreateMessage(sender, to, subject, message_text):
    """Create a message for an email.

    Args:
      sender: Email address of the sender.
      to: Email address of the receiver.
      subject: The subject of the email message.
      message_text: The text of the email message.

    Returns:
      An object containing a base64 encoded email object.
    """
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string())}


def SendMessage(service, user_id, message):
    """Send an email message.

    Args:
      service: Authorized Gmail API service instance.
      user_id: User's email address. The special value "me"
      can be used to indicate the authenticated user.
      message: Message to be sent.

    Returns:
      Sent Message.
    """
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
                   .execute())
        print 'Message Id: %s' % message['id']
        return message
    except errors.HttpError, error:
        print 'An error occurred: %s' % error

# For information on the Python Client Library visit:
#
#   https://developers.google.com/api-client-library/python/start/get_started
if __name__ == '__main__':
  main(sys.argv)
