# coding:utf-8
import multiprocessing

from multiprocessing import Queue, Process, Pool, Manager
from threading import Thread
import time
from datetime import datetime
import random
# from conf.logger import testlogger
from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.scheduler import Scheduler

# sched = Scheduler()
scheduler = BackgroundScheduler()


# @scheduler.scheduled_job('cron', id='invest_consultant_announcement_abstract', second='*/50')
@scheduler.scheduled_job('cron', id='invest_consultant_announcement_abstract', second='*/50')
@scheduler.interval_schedule(minutes=1)
def output(task):
    print("-- convert  %s %s" % (task, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import time

scheduler = BackgroundScheduler()


@scheduler.scheduled_job('cron', id="schedule_rating_adjust", minute='*/59', day_of_week='mon-fri', hour='9-20')
def schedule_rating_adjust():
    date_str = datetime.now().strftime("%Y-%m-%d")


scheduler.get_job("schedule_rating_adjust").modify(next_run_time=(datetime.now() + timedelta(seconds=1)))

scheduler.start()

if __name__ == "__main__":
    scheduler.start()
    while True:
        time.sleep(10)
