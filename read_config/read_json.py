import os
import json


def __get_parameters():
    uranus_path = os.getenv('URANUS_PATH')
    uranus_path = os.path.dirname(os.path.realpath(__file__))
    #
    # for jsons in os.listdir(uranus_path):
    print(uranus_path)
    # db_cfg = json.load(open(uranus_path))
    # db_cfg = json.load(open(uranus_path + '/etc/data.json'))
    print (os.listdir(uranus_path))
    with open(uranus_path + '/etc/data.json') as logger_json:
        logger_dict = json.load(logger_json)


__get_parameters()
