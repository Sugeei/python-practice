import os
from config.base import root_path


class Base():
    def __init__(self):
        pass

    def format(self, src):
        """

        :param src:
        :return: tickerid, city
        """
        return src[2], src[1]

    # transform()transform
