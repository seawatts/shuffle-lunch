import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apiclient import errors
import os
from shuffle.config import config


class EmailService:
    def __init__(self, google_api_service):
        self.__google_email_api = google_api_service.gmail

    def send_emails_to_groups(self, randomized_groups, email_from, email_subject, email_body):
        for group in randomized_groups:
            recipients = []
            for user in group.get_members():
                recipients.append(user.get_email())

            message = self.__create_message(email_from, recipients, email_subject, email_body)
            # By sending from 'me' it will send the message as the currently authenticated user
            self.__send_message(email_from, message)

    def send_emails_to_groups_with_template(self, randomized_groups, email_from, email_subject, email_template_file):
        self.send_emails_to_groups(randomized_groups, email_from, email_subject, self.__create_message_body(email_template_file))

    @staticmethod
    def __create_message_body(email_template_file):
        email_template_file = os.path.join(os.path.dirname(config.__file__), email_template_file)
        f = open(email_template_file)
        body = f.read()
        return body

    @staticmethod
    def __create_message(sender, recipients, subject, message_text):
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
        for recipient in recipients:
            message.add_header("to", recipient)
        message['from'] = sender
        message['subject'] = subject
        return {'raw': base64.urlsafe_b64encode(message.as_string())}

    def __send_message(self, user_id, message):
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
            message = (self.__google_email_api.users().messages().send(userId=user_id, body=message)
                       .execute())
            print('Message Id: %s' % message['id'])
            return message
        except errors.HttpError as error:
            print('An error occurred: %s' % error)
            raise error
