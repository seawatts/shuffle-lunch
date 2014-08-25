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
        shuffle_file_data = open(shuffle_file_name)
        shuffles = json.load(shuffle_file_data)
        shuffle_file_data.close()
        shuffle_models = []
        for shuffle in shuffles:
            shuffle_model = ShuffleModel.from_json(shuffle)
            shuffle_models.append(shuffle_model)
        return shuffle_models

    def __execute_shuffle(self, shuffle):
        try:
            all_accepted = self.__calendar_service.get_all_accepted_attendees(shuffle.recurring_event_id, shuffle.calendar_group_alias)
            randomized_groups = self.__randomize_service.create_randomize_groups(all_accepted, shuffle.group_size)
            self.__email_service.send_emails_to_groups_with_template(randomized_groups, shuffle.email_model.from_email, shuffle.email_model.subject, shuffle.email_model.template)

        except client.AccessTokenRefreshError:
            print("The credentials have been revoked or expired, please re-run"
                  "the application to re-authorize")

    def execute(self):
        for shuffle in self.__shuffle_models:
            logging.info("Executing shuffle lunch: " + shuffle.name)
            self.__execute_shuffle(shuffle)