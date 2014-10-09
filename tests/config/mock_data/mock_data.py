import os
from shuffle.models.group_model import GroupModel
from shuffle.models.user_model import UserModel

from shuffle.services.google_api_service import GoogleApiService
from tests.config import mock_data
from tests.utilities.json_file_helpers import get_json_from_file


class MockData:
    def __init__(self):
        pass

    __mock_data_dir = os.path.dirname(mock_data.__file__)
    __emails_data_file = os.path.join(__mock_data_dir, "emails.json")
    __attendees_accepted_data_file = os.path.join(__mock_data_dir, "attendees_accepted.json")
    __attendees_declined_file = os.path.join(__mock_data_dir, "attendees_declined.json")
    __attendees_partial_accepted_file = os.path.join(__mock_data_dir, "attendees_partial_accepted.json")
    __random_groups_file = os.path.join(__mock_data_dir, "random_groups.json")

    ATTENDEES_ACCEPTED = get_json_from_file(__attendees_accepted_data_file)
    ATTENDEES_DECLINED = get_json_from_file(__attendees_declined_file)
    ATTENDEES_PARTIAL_ACCEPTED = get_json_from_file(__attendees_partial_accepted_file)
    EMAILS = get_json_from_file(__emails_data_file)

    RANDOM_GROUPS = []
    __random_groups_from_file = get_json_from_file(__random_groups_file)
    for group in __random_groups_from_file:
        users = []
        for user in group["members"]:
            users.append(UserModel(user["email"]))

        RANDOM_GROUPS.append(GroupModel(users))

    @staticmethod
    def google_api_service():
        return GoogleApiService()
