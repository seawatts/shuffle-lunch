from datetime import datetime
import json
import logging
import os
import random
import sys
from shuffle.config import config
from shuffle.encoders.object_encoder import ObjectEncoder

from shuffle.models.group_model import GroupModel


class RandomizeService:
    def __init__(self):
        pass

    @staticmethod
    def create_randomize_groups(users, group_size):
        logging.info("Randomizing " + str(len(users)) + " users into groups of " + str(group_size))
        groups = []

        # Create copy of users so that we don't modify the original copy
        users_copy = users[:]
        # past_groups = RandomizeService.__read_groups_from_file()
        # sorted_users = RandomizeService.__sort_users(users_copy)

        # TODO: Create random algoirthm here
        # TODO: Sort the users based on some sort of weight
        current_group_size = 0
        group_members = []
        for index in range(len(users_copy)):
            random_index = random.randrange(len(users_copy))
            user = users_copy[random_index]
            group_members.append(user)
            del users_copy[random_index]
            current_group_size += 1

            if current_group_size % group_size == 0:
                groups.append(GroupModel(group_members))
                group_members = []
                current_group_size = 0
            elif len(users_copy) == 0:
                # This is for the last group
                groups.append(GroupModel(group_members))

        RandomizeService.__write_groups_to_file(groups)
        logging.info("Created " + str(len(groups)) + " groups")
        return groups


    @staticmethod
    def __write_groups_to_file(groups):
        file_path = RandomizeService.__get_group_file_path()

        with open(file_path, 'w+') as outfile:
            json.dump(groups, outfile, cls=ObjectEncoder, sort_keys=True, indent=2)

    # @staticmethod
    # def __read_groups_from_file():
    #     # read group
    #     groups = []
    #
    #     return groups

    @staticmethod
    def __get_group_directory():
        main_class_directory = os.path.dirname(sys.argv[0])
        group_directory = os.path.join(main_class_directory, config.GROUPS_BASE_FILE_LOCATION)
        if not os.path.exists(group_directory):
            os.makedirs(group_directory)
        return group_directory


    @staticmethod
    def __get_group_file_path():
        group_directory = RandomizeService.__get_group_directory()
        current_date = datetime.utcnow().strftime("%Y%m%dT190000Z")
        final_file_name = current_date + ".json"
        full_path = os.path.join(group_directory, final_file_name)
        return full_path

    @staticmethod
    def __sort_users(users):
        return users

    @staticmethod
    def __user_compare_function(user1, user2):
        return None