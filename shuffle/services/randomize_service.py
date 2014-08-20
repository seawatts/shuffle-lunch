import random
from shuffle.models.group_model import GroupModel


class RandomizeService:
    def __init__(self):
        pass

    @staticmethod
    def create_randomize_groups(users, group_size):
        groups = []

        # Create copy of users so that we don't modify the original copy
        users_copy = users[:]
        # users = self.__sort_users(users)

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

        return groups

    @staticmethod
    def __sort_users(self, users):
        return users

    @staticmethod
    def __user_compare_function(user1, user2):
        return None