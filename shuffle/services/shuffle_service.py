import json
import logging
import os

from oauth2client import client

from shuffle.config import config
from shuffle.models.shuffle_config_model import ShuffleModel
from shuffle.services.calendar_service import CalendarService
from shuffle.services.email_service import EmailService
from shuffle.services.randomize_service import RandomizeService


class ShuffleService:
    def __init__(self, shuffle_file_name, google_api_service):
        shuffle_models = self.__load_shuffle_data_file(shuffle_file_name)

        self.__shuffle_models = shuffle_models
        self.__calendar_service = CalendarService(google_api_service)
        self.__email_service = EmailService()
        self.__randomize_service = RandomizeService()

    @staticmethod
    def __load_shuffle_data_file(shuffle_file_name):
        shuffle_file_name = os.path.join(os.path.dirname(config.__file__), shuffle_file_name)
        try:
            shuffle_file_data = open(shuffle_file_name)
            shuffles = json.load(shuffle_file_data)
            shuffle_file_data.close()
        except IOError as error:
            logging.error("Could not find the shuffle config file. This is unrecoverable, please create a shuffle config file and try again. %s" % error)
            raise error

        shuffle_models = []
        for shuffle in shuffles:
            try:
                shuffle_model = ShuffleModel.from_json(shuffle)
                shuffle_models.append(shuffle_model)
            except IOError as error:
                logging.error("Could not read the shuffle config file. This is unrecoverable, please check syntax of shuffle config file and try again. %s" % error)
                raise error

        return shuffle_models

    def __execute_shuffle(self, shuffle, is_dev_environment):
        try:
            all_accepted = self.__calendar_service.get_all_accepted_attendees(shuffle.recurring_event_id, shuffle.calendar_group_alias)
        except Exception as error:
            logging.error("Could not execute getting all accepted attendees. This is unrecoverable, please check configuration and try again. %s" % error)
            return

        try:
            randomized_groups = self.__randomize_service.create_randomize_groups(all_accepted, shuffle.group_size)
        except Exception as error:
            logging.error("Could not create randomized groups. This is unrecoverable, please check configuration and try again. %s" % error)
            return

        # Don't email the users if we are in a dev environment
        if is_dev_environment:
            return

        try:
            self.__email_service.send_emails_to_groups_with_template(randomized_groups, shuffle.email_model.from_email, shuffle.email_model.subject, shuffle.email_model.template)
        except Exception as error:
            logging.error("Could not execute sending emails to groups. This is unrecoverable, please check configuration and try again. %s" % error)
            return

    def execute(self, is_dev_environment=False):
        for shuffle in self.__shuffle_models:
            logging.info("Executing shuffle: " + shuffle.name)
            self.__execute_shuffle(shuffle, is_dev_environment)
            logging.info("Finished executing shuffle: " + shuffle.name)
