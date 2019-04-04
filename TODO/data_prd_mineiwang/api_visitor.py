# coding: utf8

# In[1]:

import requests
import types

from common.config import logger


class APIVisitor(object):
    SECID_SIZE = 200  # 接收数组参数的最大长度

    def __init__(self, token, url, username="", params={}):
        """

        :param token:
        :param url:
        :param username:
        :param params:  api url 查询使用的所有key, 传入一个dict
        """
        self.token = token
        self.url = url
        self.username = username
        self.params = params
        # self.cfg = Config()

    def toStr(self, val):
        if val is None:
            val = ""
        elif isinstance(val, types.ListType):
            # elif type(val) is types.ListType:
            val = ",".join(val)
        elif isinstance(val, types.IntType):
            # elif type(val) is types.IntType:
            val = str(val)
        return val.decode("utf8")

    def getcontent(self, params):
        """

        :param params: piMedicinalname=&piBigsortid=&piBigsortname=&piMedicineparentid=&piMedicineparentname=&piS
        :return:
        """
        # Todo how to merge two dict, I mean merge, you know
        for key, value in params.items():
            self.params[key] = value
        paramStr = ["%s=%s" % (key, self.toStr(self.params[key])) for key in self.params.keys()]
        info = "&".join(paramStr)
        api = "%s?%s" % (self.url, info)  # "/api/%s/%s.json?%s" % (api_type, api_name, searches)
        # logger.info(u"get data with api %s" % self.url)
        print("getcontent api is %s" % api)
        logger.info("getcontent api is %s" % api)
        resp = requests.get(url=api, headers={"username": self.username,
                                              "token": self.token}, verify=False)
        code, ret_json = resp.status_code, resp.json()
        if code == 200 and ret_json['retCode'] == 1:
            return ret_json['data']
        # else:
        #     logger.info(u"failed with http status code %s and response content %s, url %s"
        #                 % (code, json.dumps(ret_json, ensure_ascii=False), api))
        return None
