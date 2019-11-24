import os
import requests
import StringIO
import pandas as pd

api_prefix = os.environ.get('API_PREFIX', "https://api.wmcloud.com/data/v1")
api_token = os.environ.get('API_TOKEN', 'e63e9c73146c83b48bf967863de8a9125cdd3c83539739f1090f2ae81dad5dd6')


def __api_req__(path, params):
    param_strs = []
    for k, v in params.items():
        param_strs.append('%s=%s' % (k, v))
    url = api_prefix + path + "?" + '&'.join(param_strs)
    # print url
    resp = requests.get(url=url, headers={"Authorization": "Bearer %s" % api_token})
    output = StringIO.StringIO()
    output.write(resp.text)
    output.seek(0)
    df = pd.read_csv(output)
    return df


def stock_factors_one_day(**kwargs):
    return __api_req__("/api/market/getStockFactorsOneDay.csv", kwargs)


def stock_factors_date_range(**kwargs):
    return __api_req__("/api/market/getStockFactorsDateRange.csv", kwargs)


def sec_halt(**kwargs):
    return __api_req__("/api/master/getSecHalt.csv", kwargs)


def equ(**kwargs):
    return __api_req__("/api/equity/getEqu.csv", kwargs)


def trade_cal(**kwargs):
    return __api_req__("/api/master/getTradeCal.csv", kwargs)


if __name__ == '__main__':
    print stock_factors_one_day(ticker="000001,600000", tradeDate="20180309", field='secID,MA5')
