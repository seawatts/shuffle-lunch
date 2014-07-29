import argparse
import base64
from datetime import datetime
from email import errors
from email.mime.text import MIMEText
import os
import sys

import httplib2
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
EMAIL_BODY_TEMPLATE_FILE = "email-template.txt"
USER_GROUP_FILE_PREFIX = "get current date or something.txt"
GROUP_SIZE = 5


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
        all_accepted = get_all_accepted_attendees(calendar, admin)
        randomized_groups = create_randomize_groups(all_accepted)
        # randomized_groups = [['cwatts@simplymeasured.com']]
        send_emails_to_groups(gmail, randomized_groups)

    except client.AccessTokenRefreshError:
        print ("The credentials have been revoked or expired, please re-run"
               "the application to re-authorize")


def get_all_accepted_attendees(calendar, admin):
    all_accepted = []
    emails = admin.members().list(groupKey=ALL_GROUP_ALIAS).execute()

    # TODO: Loop through all the emails in the 'all' alias and get each event to see if they have accepted
    for users_email in emails:
        # print email['email']
        # usersEmail = "cwatts@" + DOMAIN
        event_id = compose_event_id()
        event = calendar.events().get(calendarId=users_email, eventId=event_id).execute()
        attendees = event['attendees']
        accepted = get_accepted_attendees(users_email, attendees)
        all_accepted.append(accepted)

    return all_accepted


def compose_event_id():
    current_date = datetime.utcnow().strftime("%Y%m%dT190000Z")
    return RECURRING_EVENT_ID + "_" + current_date


def get_accepted_attendees(users_email, attendees):
    accepted = []
    declined = []
    needs_action = []

    # NOTE: This should actually only return one name
    for attendee in attendees:
        if attendee['email'] == users_email:
            response_status = attendee['responseStatus']
            if response_status == 'accepted':
                accepted.append(attendee)
            elif response_status == 'declined':
                declined.append(attendee)
            elif response_status == 'needsAction':
                needs_action.append(attendee)

            continue

    print 'accepted {}'.format(len(accepted))
    print 'needsAction {}'.format(len(needs_action))
    print 'declined {}'.format(len(declined))

    return accepted


def create_randomize_groups(users):
    groups = []
    users = sort_users(users)
    # TODO: Create random algoirthm here
    # TODO: Sort the users based on some sort of weight
    current_group_size = 0
    group = []
    for user in users:
        group.append(user)
        current_group_size += 1

        if current_group_size % GROUP_SIZE == 0:
            groups.append(group)
            group = []
            current_group_size = 0

    return groups


def sort_users(users):

    pass


def user_compare_function(user1, user2):
    return


def write_user_groups_to_file(group):
    f = open(USER_GROUP_FILE_PREFIX, "w")
    f.write(group)
    f.close()


def send_emails_to_groups(gmail, randomized_groups):
    for group in randomized_groups:
        # TODO: Combine emails into one email
        for user in group:
            email_to = user
            message = create_message(EMAIL_FROM, email_to, EMAIL_SUBJECT, create_message_body())
            # By sending from 'me' it will send the message as the currently authenticated user
            send_message(gmail, 'me', message)


def create_message_body():
    f = open(EMAIL_BODY_TEMPLATE_FILE)
    body = f.read()
    return body


def create_message(sender, to, subject, message_text):
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


def send_message(service, user_id, message):
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

if __name__ == '__main__':
    main(sys.argv)
