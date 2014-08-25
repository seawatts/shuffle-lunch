import json


def get_json_from_file(file_name):
    json_data = open(file_name)

    data = json.load(json_data)
    json_data.close()

    return data