# coding=utf8
import json
import time
from threading import Thread


class MsgProducer(Thread):
    def __init__(self):
        super(MsgProducer, self).__init__()

        self.exchange = "test_exchange"
        # self.exchange.connect()

    def run(self):
        queue = "test_queue_pdf2html"
        exchange = "test_pdf2html"
        channel = self.exchange.connect()
        channel.queue_declare(queue=queue, durable=True)
        channel.queue_bind(queue, exchange)

        while True:
            rp_msg = {
                "data_value": time.time(),
            }
            message_str = json.dumps(rp_msg, ensure_ascii=False, encoding="utf-8")
            channel.basic_publish(exchange, queue, message_str.encode("utf8"))
            time.sleep(1)
            print("msg produced")


MsgProducer().start()


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    # import time
    # time.sleep(10)
    print 'ok'
    ch.basic_ack(delivery_tag=method.delivery_tag)


class NewTask(Thread):
    """
    Get tasks from MQ, record in mongo
    """

    def __init__(self, queuename):
        super(NewTask, self).__init__()
        self.mongodb = mongodb
        self.exchange = source_msg_exchange
        self.channel = self.exchange.connect()
        self.queue = queuename

    def declare_queue(self, queuename):
        # self.exchange.connect()
        # self.exchange.channel.queue_declare(queue=queuename)
        # self.exchange.connect()
        self.channel = self.exchange.connect()
        self.queue = queuename

        # connection = self.exchange.connect()
        # self.channel = self.exchange.channel
        # Get ten messages and break out
        # make message persistent
        #
        # queue_state = channel.exchange_declare(exchange='test_pdf2html',
        #                          type="topic",
        #                          durable=True,
        #                          auto_delete=False)
        # queue_empty = queue_state.method.message_count == 0
        # channel.queue_declare(queue=queuename)
        # # if not queue_empty:
        # while True:
        #     method, properties, body = channel.basic_get(queuename, no_ack=True)
        #     callback(channel, method, properties, body)
        #     print(' [*] Waiting for messages. To exit press CTRL+C')
        # channel.start_consuming()

    def run(self):
        """
        1. timestamp
        2. produce taskId
        :return:
        """
        # self.declare_queue()

        for method_frame, properties, body in self.channel.consume(self.queue):
            # Display the message parts
            # print(method_frame)
            # print(properties)
            print("consume" + body)

            # Acknowledge the message
            self.channel.basic_ack(method_frame.delivery_tag)

        #
        # while True:
        #     msg = self.exchange.channel.basic_consume(queue="test_queue_pdf2html", no_ack=True)
        #
        # logger.info('get request %s' % json.dumps(task, ensure_ascii=False, encoding="utf-8"))
        #
        # report_id = task['announcement_id']
        # pdf_addr = task['pdf_addr']
        # title = task['title']
        # tool = task.get['tool']
        # publish_date = datetime.strptime(time.strftime('%Y-%m-%d'), '%Y-%m-%d')
        #
        # zsAutoCategory = task['zsAutoCategory']
        #
        # task_id = util.base64_md5(pdf_addr + "_" + tool)
        #
        # submitTime = time.time()
        # submitTimePretty = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(submitTime))
        #
        # # dest_file = os.path.join(origin
        # # 提交任务到mongo中， 置状态为 undo
        # dict_hash = {
        #     "reportId": report_id,
        #     "taskId": task_id,
        #     "progress": taskstatus.SUBMIT,
        #     "pdf_address": pdf_addr,
        #     "submitTime": submitTime,
        #     "submitTimePretty": submitTimePretty,
        #     # "pdf_path": dest_file,
        #     "publishDate": publish_date,
        #     "title": title,
        #     "tool": tool,
        #     # "outfile": '',
        #     # "mode": mode,
        #     "zsAutoCategory": zsAutoCategory,
        # }
        # self.mongodb.reports_db.solid_pdfs.update({"taskId": task_id}, dict_hash, True, True)


task = NewTask("test_queue_pdf2html")
# task.declare_queue("test_queue_pdf2html")
task.start()
