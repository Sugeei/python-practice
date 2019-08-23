from .celery_conf import app, logging


@app.task(bind=True, typing=False)
def add(self, x, y):
    logging.info("start add , %s" % self)
    result = x+y
    print result
    return result


@app.task()
def mul(x, y):
    result = x * y
    print result
    return result


@app.task(bind=True)
def xsum(numbers):
    return sum(numbers)

