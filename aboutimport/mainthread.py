import time
from datetime import datetime, timedelta
from threading import Thread
from multiprocessing import Process

class Demo(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            p = Process()

# cfg = Config()
# cacher = Cache()


# TODO
# 按实际要刷的日期修改


# cache dates for three years by default
# TODO 需要一个类去整合数据集， 一部分从cache中来， 一部分从数据库中直接读


# @scheduler.scheduled_job('cron', id="base_consensus", day_of_week='mon-fri', hour='23', minute='10')
# TODO for debug
# schedule 的两个任务只做当天的。
@scheduler.scheduled_job('cron', id="base_consensus", hour='22', minute='30')
def base_consensus():
    curdate = datetime.now().strftime("%Y-%m-%d")
    logger.info("daily consensus run on %s" % curdate)
    dataset = loader.increment_update((datetime.now() - timedelta(days=300)).strftime("%Y-%m-%d"))
    simple_calculation(curdate, dataset)


# TO cache data of current day
# @scheduler.scheduled_job('cron', id="cache_consensus", hour='*/2')
# def cache_consensus():
#     curdate = datetime.now().strftime("%Y-%m-%d")
#     logger.info("cache consensus run")
#     updated_dataset = cacheday(curdate)
#     # TODO 更新缓存时找出那些有修改的记录， 保存下来， 重刷相关数据
#     update_operation(updated_dataset)


collection = "consensus_history"


class OperHis(Thread):
    def __init__(self, queue=None, statusqueue=None):
        Thread.__init__(self)
        Thread.setName(self, "consensu_history")
        self.queue = queue
        self.statusqueue = statusqueue
        self.dataset = {}

    @property
    def set_dataset(self, dataset):
        self.dataset = dataset

    def run(self):
        # start_date = '2007-01-01'
        # start_date = '2010-01-01'
        # logger.info('add new task to mongo ')

        # TODO 从哪天开始读就写哪天
        # TODO 防止上线的时候忘记改回来
        ti = time.time()
        logger.info('read sql from date %s ' % cfg.consensus_date)
        # try:
        #     # raise ValueError
        #     self.dataset = pd.read_pickle('src/dataset20190807.pkl')
        # except:
        #     pass
        self.dataset = loader.increment_update(start_date=cfg.consensus_date)

        import pickle
        with open('dataset.pkl', 'wb') as f:
            pickle.dump(self.dataset, f, protocol=pickle.HIGHEST_PROTOCOL)

        for key in self.dataset.keys():
            logger.info("source data (%s, length=%s)" % (key, len(self.dataset[key])))
        logger.info('read sql time %s ' % int(time.time() - ti))
        #
        # # schedule 依赖前一天的计算结果， 所以一次性算完
        # start_date = '2010-01-01'
        # # start_date = '2019-01-01'
        # end_date = datetime.today().strftime("%Y-%m-%d")
        # ced_calculator = OperSch(start_date=start_date, end_date=end_date)
        # ced_calculator.data_set = self.dataset
        # for result in ced_calculator.cal_history():
        #     d = result.con_date.unique().tolist()[0]
        #     cacher.cache(result, 'schedule_pre', convert_score(d))
        #     logger.info('schedule get result on %s to %s, length is %s' % (d, '', len(result)))
        # logger.info('[ main ] schedule get result from %s to %s, length is %s' % (start_date, end_date, len(result)))
        # write_schedule(result)

        res_list = []
        while True:
            # 从mongo中取任务， 按date正序取。 schedule需要正序算
            result = cfg.mongolazy.connect().get_collection(collection).find_one_and_update(
                {'status': 'wait'},
                {"$set": {'status': 'doing',
                          'processtime': time.time()}},
                sort=[("date", 1)]
            )
            if result is None:
                time.sleep(10)
                continue
            pre_date = result['date']
            logger.info('get task on %s' % pre_date)
            # simple_calculation(pre_date, self.dataset)

            p = Process(target=simple_calculation,
                        args=(pre_date, self.dataset,))
            # operation(curdate, resultqueue)
            p.start()
            res_list.append(p)
            logger.info("alive processes %s" % len(res_list))
            while len(res_list) >= int(cfg.consensus_processes):  # 内存限制16G, 每个process要2.5G朝上， 所以最多并行4个啦
                res_list = [p for p in res_list if p.is_alive()]
                # TODO 下面不用一直打印
                time.sleep(1)

    # TODO 取少量数据并没有什么用。。。
    def thin_dataset(self, pre_date):
        # start_date = str(int(pre_date[0:4]) - 1) + '-01-01'
        start_date = (datetime.strptime(pre_date, '%Y-%m-%d') - timedelta(days=300)).strftime('%Y-%m-%d')
        # thindataset = {}
        # for key in self.dataset.keys():
        #     thindataset[key] =
        subset = {}
        # colmap = KeyMap().date_column
        for key in self.dataset.keys():
            df = self.dataset[key]
            if keymap.get(key) is not None:
                subset[key] = df[(df[keymap.get(key)] >= start_date) & (df[keymap.get(key)] <= pre_date)]
            else:
                subset[key] = df
        return subset


class Newtask(Thread):
    def __init__(self):
        Thread.__init__(self)
        Thread.setName(self, "Newtask")
        # self.queue = queue
        # self.statusqueue = statusqueue
        self.dataset = {}

    def run(self):
        start_date = '2007-01-01'
        # start_date = '2010-01-01'
        ti = time.time()
        # logger.info('add new task to mongo ')

        trade_list = pd.date_range(start='2010-01-01', end=datetime.now().strftime("%Y-%m-%d")).astype(str).tolist()
        for d in trade_list:
            try:
                logger.info('add new task to mongo %s' % d)
                cfg.mongo.mongo_db.get_collection(collection).insert_one({
                    'date': d,
                    'status': 'wait'
                })

            except:
                pass
        # # TODO 从哪天开始算就写哪天




def main_batch_history():
    ti = time.time()
    logger.info('read sql from date %s ' % cfg.consensus_date)

    dataset = loader.increment_update(start_date=cfg.consensus_date)

    end_date = datetime.today().strftime('%Y-%m-%d')

    resultstk, result = batch_calculation(cfg.consensus_date, end_date, dataset)

    logger.info("write result to stk")
    t = time.time()
    write_stk(resultstk)
    logger.info("write result to stk done %s " % int(time.time() - t))
    logger.info("write result to schedule")
    t = time.time()
    write_schedule(result)
    logger.info("write result to schedule done %s " % int(time.time() - t))


# 这里不缓存数据，直接读
# mongo 中存需要计算的日期， 一个日期一个任务 ，
# 缓存任务这边直接从07年读入数据。

# 最小的修改是全部数据读入后， 分年存储， 计算的时候只传需要的部分数据
if __name__ == "__main__":
    # reset_cache_date()
    curdate = datetime.now().strftime("%Y-%m-%d")
    # logger.info("cache consensus run")

    # scheduler.get_job("base_consensus").modify(next_run_time=(datetime.now() + timedelta(seconds=1)))
    # scheduler.get_job("base_consensus").modify(next_run_time=(datetime.now() + timedelta(seconds=1)))
    # # scheduler.get_job("cache_consensus").modify(next_run_time=(datetime.now() + timedelta(seconds=1)))
    # scheduler.start()
    from base_consensus.src.consen_operator import batch_calculation
    # dataset = loader.increment_update(start_date=cfg.consensus_date)
    dataset = pd.read_pickle('dataset.pkl')
    end_date = datetime.today().strftime('%Y-%m-%d')
    resultstk, result = batch_calculation(cfg.consensus_date, end_date, dataset)
    logger.info("write result to stk")
    t = time.time()
    write_stk(resultstk)
    logger.info("write result to stk done %s " % int(time.time() - t))
    logger.info("write result to schedule")
    t = time.time()
    write_schedule(result)
    logger.info("write result to schedule done %s " % int(time.time() - t))

    # 这个队列只用来传输任务状态了， 算完一天就加个消息到里面， writer收到消息后去redis里取数据，再写库
    # 这个queue不太靠谱， 重启就没了，
    # TODO 用外部的MQ
    resultqueue = Manager().Queue()
    # statusqueue = Manager().Queue()

    OperHis(resultqueue).start()
    # StatusTrack(statusqueue).start()
    Writer(exchange=cfg.consensus_exchange, exqueue=cfg.consensus_queue).start()
    # Writer(resultqueue).start()
    # Newtask().start()
    while True:
        time.sleep(100)
    # 计算结果存redis, 发消息到队列

# TODO 测运行时长
# # 运行计时 alive processes 1
# 2019-08-30 16:27:25,823 [INFO] consensu_history Line:226 - simple_calculation start on 2018-03-23
# 2019-08-30 16:27:25,855 [INFO] consensu_history Line:69 - Begin to calculate ticker: all from to
# 2019-08-30 16:27:25,857 [INFO] consensu_history Line:97 - Begin to get data...
# 2019-08-30 16:27:25,875 [INFO] consensu_history Line:112 - get task on 2018-03-22
# 2019-08-30 16:27:26,038 [INFO] consensu_history Line:120 - alive processes 2
# 2019-08-30 16:27:26,059 [INFO] consensu_history Line:226 - simple_calculation start on 2018-03-22
# 2019-08-30 16:27:26,086 [INFO] consensu_history Line:69 - Begin to calculate ticker: all from to
# 2019-08-30 16:27:26,088 [INFO] consensu_history Line:97 - Begin to get data...

#
# 2019-08-30 17:11:51,485 [INFO] consensu_history Line:120 - alive processes 2
# 2019-08-30 17:11:51,494 [INFO] consensu_history Line:226 - simple_calculation start on 2017-12-26
# 2019-08-30 17:11:51,520 [INFO] consensu_history Line:69 - Begin to calculate ticker: all from to
# 2019-08-30 17:11:51,526 [INFO] consensu_history Line:97 - Begin to get data...

# 半小时跑3个月数据
