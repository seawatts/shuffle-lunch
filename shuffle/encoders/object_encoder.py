import json


class ObjectEncoder(json.JSONEncoder):
    def default(self, object_to_encode):
        return object_to_encode.__dict__