import logging
import os

from mandrill import Mandrill, Error
import pystache

from shuffle.config import config
from shuffle.services.gravatar_service import GravatarService


class EmailService:
    def __init__(self):
        self.__email_api = Mandrill(config.MANDRILL_API_KEY)

    def send_emails_to_groups_with_template(self, shuffle, randomized_groups):
        logging.info("Emailing groups")
        for group in randomized_groups:
            recipients = []
            template_recipients = {"recipients": []}
            for user in group.get_members():
                recipients.append({
                    "email": user.get_email(),
                    "type": "to",
                })

                template_recipients["recipients"].append({
                    "gravatar_link": GravatarService.get_gravatar_link(user.get_email()),
                    "email": user.get_email(),
                    "shuffle_name": shuffle.name
                })

            email_body = self.__create_message_body(shuffle.email_model.template, template_recipients)
            message = self.__create_message(shuffle.email_model.from_email, recipients, shuffle.email_model.subject, email_body)
            # By sending from 'me' it will send the message as the currently authenticated user
            self.__send_message(message)


    @staticmethod
    def __create_message_body(email_template_file, recipients):
        try:
            renderer = pystache.Renderer(search_dirs=config.EMAIL_TEMPLATES_FOLDER, partials={"header":"header.mustache", "footer":"footer.mustache"})
            template_body = renderer.render_name(email_template_file, recipients)
        except IOError as error:
            logging.error("Could not find the email template file. This is unrecoverable, please create a email template file and try again. {0}".format(error))
            raise error

        return template_body

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
            "html": message_text,
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
        logging.debug("Sending message")
        try:
            message = self.__email_api.messages.send(message=message)
            return message
        except Error as error:
            logging.error('An error occurred emailing a user: {0}'.format(error))
            raise error
