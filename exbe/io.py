import json
import os


def load_jsons(dir_name):
    filenames = os.listdir(dir_name)

    filenames = list(filter(lambda filename: filename.endswith(".json"), filenames))

    data = []
    for filename in filenames:
        with open(os.path.join(dir_name, filename), "r") as file:
            data_ = json.load(file)

        data.append(data_)

    return data
