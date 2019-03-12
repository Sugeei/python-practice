# coding=utf8
import configparser

fname = "const.properties"
config = configparser.ConfigParser()
config_file = open(fname, encoding="utf8")
# config.read("const.properties")
config.read(config_file)
print config['DEFAULT']