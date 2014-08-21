import os

from mandrill import Mandrill, Error

from shuffle.config import config


class EmailService:
    def __init__(self):
        self.__email_api = Mandrill(config.MANDRILL_API_KEY)

    def send_emails_to_groups(self, randomized_groups, email_from, email_subject, email_body):
        for group in randomized_groups:
            recipients = []
            for user in group.get_members():
                recipients.append({
                    "email": user.get_email(),
                    "type": "to"
                })

            message = self.__create_message(email_from, recipients, email_subject, email_body)
            # By sending from 'me' it will send the message as the currently authenticated user
            self.__send_message(message)

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
        message = {
            "to": recipients,
            "from_email": sender,
            "subject": subject,
            "text": message_text
        }

        return message

    def __send_message(self, message):
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
            message = self.__email_api.messages.send(message=message)
            return message
        except Error as error:
            print('An error occurred: %s' % error)
            raise error
