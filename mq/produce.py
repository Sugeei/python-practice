from common.logger import logger
from common.config import cfg

import json


class MqConn(object):
    def __init__(self, mq_url):
        # format: username:password@host:port/virtual_host
        m = re.match(r"(?P<username>.+):(?P<password>.+)@(?P<host>.+):(?P<port>\d+)/?(?P<virtual_host>.*)", mq_url)
        self.mq = {"host": m.group("host"), "port": int(m.group("port")), "username": m.group("username"),
                   "password": m.group("password"), "virtual_host": m.group("virtual_host")}
        self.virtual_host = None if (self.mq['virtual_host'] is None or len(self.mq['virtual_host']) == 0) \
            else self.mq['virtual_host']
        # self.queuename = self.mq['queuename']
        self.channel = None
        self.mq_conn = None

    def connect(self):
        # print(u"trying to connect mq with configuration %s" % self.__str__())
        self.mq_conn = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.mq['host'], port=self.mq['port'], virtual_host=self.virtual_host,
                                      # heartbeat_interval=0,
                                      credentials=pika.PlainCredentials(self.mq['username'], self.mq['password'])))
        self.channel = self.mq_conn.channel()
        return self.channel

    def close(self):
        self.mq_conn.close()

    def __str__(self):
        return json.dumps(self.mq, ensure_ascii=False, encoding='utf-8')


def inform(message_str):
    try:
        # message_str = json.dumps(message_str)
        # message_str = json.dumps(body, ensure_ascii=False)
        # logger.info("[ inform ] message_str %s" % message_str)
        channel = cfg.consensus_exchange.connect()
        # channel.queue_declare(queue=cfg.consensus_queue)
        channel.basic_publish(cfg.consensus_queue, "", json.dumps(message_str))
        logger.info("[ informed queue=%s ] %s" % (cfg.consensus_queue, message_str))
        return True
    except Exception as err:
        logger.warning("inform exception err %s" % err)
        return False
