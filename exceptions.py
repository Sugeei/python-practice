from bs4 import BeautifulSoup

ERROR_MAP = {
    "200000": "invalid input parameter",
    "500000": "load data error",
    "600000": "dump data error",
    "700000": "data verify error",
    "800000": "algorithm error"
}


class UranusError(Exception):
    def __init__(self, error_code=None, message=''):
        Exception.__init__(self,
                           '%s%s' % (ERROR_MAP[error_code] if ERROR_MAP.get(
                               error_code) is not None else '', message))
        self.error_code = error_code


# assertion
# https://realpython.com/python-exceptions/
def divide(a, b):
    try:
        r = a / b
    except:
        raise ValueError
    else:
        print('divide result is %s' % r)
    finally:
        print("done")

divide(4,0)
