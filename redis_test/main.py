# coding=utf8
import redis
import os
import pandas as pd
from datetime import datetime
import json

# TODO about how to store df into redis, and the data will be updated time after time
# redis_pool = redis.ConnectionPool(host=os.environ.get("REDIS", "redis"), port=6379, decode_responses=True)
redis_pool = redis.ConnectionPool(host='localhost', port=6379, db=0, decode_responses=True)

org_predict_df = pd.read_csv("org_predict.csv", index_col=0, dtype={"ticker_symbol": str})
org_predict_df = org_predict_df.dropna(subset=['time_year'])
org_predict_df['time_year'] = org_predict_df['time_year'].astype(int)


def redis_connect():
    r = redis.Redis(connection_pool=redis_pool)
    return r


r = redis_connect()
r.zadd("test", 'abc', 1)


#


def pop_redis(key, score):
    redis = redis_connect()
    result_list = redis.zrevrangebyscore(key, score, score)

    # To remove from redis
    redis.zremrangebyscore(key, score, score)
    return result_list


def get_redis(key):
    redis = redis_connect()
    # return redis.get(key)
    return redis.zrange(key, 0, 999999999)


def put_redis(key, score, data):
    redis = redis_connect()
    redis.zadd(key, data, score)
    # for item in data_list:


def range_store(key, scorename, data):
    """
    将整张表缓存在redis中
    :param key:
    :param scorename:
    :param data:
    :return:
    """

    for i in range(len(data)):
        # 逐条存储， 用create date + ticker_symbol做 key
        row = data.iloc[i]
        score = row[scorename]
        # createdate = datetime.strptime(row['create_date'], "%Y-%m-%d").strftime("%Y%m%d")
        # score = int(str(year) + ticker + str(org))
        put_redis(key, score, row.to_json(orient='records'))


def range_read(key, cloumns=None):
    """
    从redis中读出整个key拼成df
    :param key:
    :param score:
    :return:
    """
    df = pd.DataFrame()
    data = get_redis(key)
    for item in get_redis(key):
        df.append(pd.DataFrame([json.loads(item)]))
        df.append(pd.DataFrame(data)）

    return df


if __name__ == "__main__":

    # range_store('org_predict', "report_search_id", org_predict_df)
    org_predict_df.columns
    #
    df = range_read('org_predict', org_predict_df.columns)
    # for i in range(len(data)):
    #     # 逐条存储， 用create date + ticker_symbol做 key
    #     row = org_predict_df.iloc[i]
    #     ticker = row['ticker_symbol']
    #     year = row['time_year']
    #     org = row['organ_id']
    #     createdate = datetime.strptime(row['create_date'], "%Y-%m-%d").strftime("%Y%m%d")
    #     score = int(str(year) + ticker + str(org))
    #     put_redis("org_predict", score, row.to_json())
    #     # put_redis("org_predict", 101, "bbb")
    #     # a=get_redis("org_predict", 101)
    #     # r=redis_connect()
    #     # r.zrevrangebyscore("org_predict", 100, 100)
    #     # a = get_redis("org_predict", score)
    #     for item in get_redis("org_predict", score):
    #         pd.DataFrame([json.loads(item)])

# return json.dumps({str(self.dt): self.detail_dict}, ensure_ascii=False, encoding='utf-8')
