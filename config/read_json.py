import os
import json

def __get_parameters():
    uranus_path = os.getenv('URANUS_PATH')
    uranus_path = os.path.dirname(os.path.realpath(__file__))
    # uranus_path = os.path.dirname('consensuus_config.json')
    uranus_path = os.path.join(uranus_path, 'consensus_config.json')
    #
    # for jsons in os.listdir(uranus_path):
    print(uranus_path)
    # db_cfg = json.load(open(uranus_path))
    # db_cfg = json.load(open(uranus_path + '/etc/data.json'))
    # print (os.listdir(uranus_path))
    with open(uranus_path) as logger_json:
        logger_dict = json.load(logger_json)
        print(logger_dict)

__get_parameters()