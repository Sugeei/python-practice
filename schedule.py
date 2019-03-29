from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import time

scheduler = BackgroundScheduler()


@scheduler.scheduled_job('cron', id="schedule_rating_adjust", minute='*/59', day_of_week='mon-fri', hour='9-20')
def schedule_rating_adjust():
    date_str = datetime.now().strftime("%Y-%m-%d")


scheduler.get_job("schedule_rating_adjust").modify(next_run_time=(datetime.now() + timedelta(seconds=1)))

scheduler.start()
