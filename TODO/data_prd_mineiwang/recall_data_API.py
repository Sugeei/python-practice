# coding: utf8

# In[1]:

from data_loader import DBConn
import pandas as pd

# from lib.config import Config, logger
# from utils import data_api_prefix
from pandas import DataFrame
import pandas as pd
from bson import json_util as json
import requests
import types

import db_base
import add_crc as crc

from common.logger import logger
base = db_base.DB_Base()


class MysqlConn(object):
    def __init__(self, config_json_str):
        # self.mysql_config = {"host": "10.22.128.150",  "port": 3317, "db": "bigdata", "user": "talend_load",
        #   "passwd": "s9t5gNThn2vqWM7c" , "charset" : "utf8"}
        # self.mysql_config = {"host": "db-bigdata.wmcloud-qa.com",  "port": 3312, "db": "bigdata", "user": "app_bigdata_ro",
        #   "passwd": "Welcome_20141217"}
        self.mysql_config = json.loads(config_json_str, encoding='utf-8')

    def connect(self):
        mysql_conn = pymysql.connect(**self.mysql_config)
        return mysql_conn


class MssqlConn(object):
    def __init__(self, config_json_str):
        # self.mssql_config = {"server": "sh-datayesdb.wmcloud-dev.com",  "port": 1433, "database": "datayesdb",
        #     "user": "talend_load", "password": "Welcome01"}
        self.mssql_config = json.loads(config_json_str, encoding='utf-8')

    def connect(self):
        mssql_conn = pymssql.connect(**self.mssql_config)
        return mssql_conn

    def __str__(self):
        return json.dumps(self.mssql_config, ensure_ascii=False, encoding='utf-8')


# In[2]:


import json
import pymysql
import pymssql

# MySQL
# bigdata={"host":"security03-dev.datayes.com","port":3306,"user":"talend_load","passwd":"NCph1G9BQT3DuQj","db":"bigdata","charset":"utf8"}
# dateyesdbp={"host":"db-datayesdb-ro.wmcloud.com","port":3313,"user":"app_dataqa_ro","passwd":"Welcome20140820","db":"datayesdbp","charset":"utf8"}

# # dateyesdbp={"host":"db-datayesdb.wmcloud.com","port":3312,"user":"app_marketdata","passwd":"JDFJ8dfasd8aKfu","db":"datayesdbp","charset":"utf8"}

# SQLserverdb-mssql02.datayes-stg.com
health_40 = {"server": "db-mssql02.datayes-stg.com", "port": 1433, "database": "health", "user": "talend_load",
             "password": "s9t5gNThn2vqWM7c", "charset": "utf8"}

# bigdata_conn = MysqlConn(json.dumps(bigdata)).connect()
# dateyesdbp_conn = MysqlConn(json.dumps(dateyesdbp)).connect()

health_conn = MssqlConn(json.dumps(health_40)).connect()

from lib_com.db_base import DB_Base


# base = DB_Base()

# In[3]:


class APIVisitor(object):
    SECID_SIZE = 200  # 接收数组参数的最大长度

    def __init__(self, token, url, username=""):
        self.token = token
        self.url = url
        self.username = username
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
        paramStr = ["%s=%s" % (key, self.toStr(params[key])) for key in params.keys()]
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


# In[4]:


# authetification
username = "rrp"
token = "37468D37D9CE3B7B36749FACF712C245"

# In[26]:

# getCiDrugsclassification = "https://124.172.190.114:8443/api/health/getCiDrugsclassification.json?FIELD=&piID=&piMedicinalname=&piBigsortid=&piBigsortname=&piMedicineparentid=&piMedicineparentname=&piS"
getCiDrugsclassification = "https://124.172.190.114:8443/api/health/getCiDrugsclassification.json"
# key:PI＿ID
params = {
    "FIELD": "",
    "piID": "",
    "piMedicinalname": "",
    "piBigsortid": ""
}


def access_api(apiurl, params, username="", token=""):
    visitor = APIVisitor(token, apiurl, username)
    data = visitor.getcontent(params)

    df_data = pd.DataFrame(data)
    # for i, item in enumerate(data):
    #     df = pd.DataFrame(item, index=[i])
    #     df_data = df_data.append(df)
    return df_data

    # In[71]:


# In[7]:
# drugsclassification[0]


# In[67]:


def write_db(base, table, df_data, pkeys, where_condition=""):
    if df_data is None or len(df_data) == 0:
        return
    # table = 'ci_drugsclassification'
    # pkeys must be a list with primary key of the table
    result = crc.add_crc(
        df_data,
        df_data.columns,
        health_conn,
        table,
        'mssql')

    base.merge_table(
        result,
        table,
        pkeys,
        where_condition,
        health_conn)


# df_drugsclassification.head()
# df_drugsclassification.info()


# In[68]:


# In[70]:


# df_drugsclassification.columns= df_drugsclassification_columns


# In[10]:


# import pandas as pd

# to get party_id list
sql = """
select *
from ci_drugsclassification where create_time<'2019-02-22' and update_time >='2019-02-22'
"""
# data = pd.read_sql(sql, conn)
# data.columns


# In[69]:

# *****************************************************************
# TODO
df_drugsclassification = access_api(getCiDrugsclassification, params, username, token)
df_drugsclassification_columns = df_drugsclassification.columns
#
df_drugsclassification.columns = [u'PI_BIGSORTID', u'PI_BIGSORTNAME', u'PI_ID', u'PI_MEDICINALATCCODE',
                                  u'PI_MEDICINALNAME', u'PI_MEDICINEPARENTID', u'PI_MEDICINEPARENTNAME',
                                  u'PI_SMALLSORTID', u'PI_SMALLSORTNAME', u'PMD_CLASS']
# df_drugsclassification.head()
table = 'ci_drugsclassification'

# ci_drugsclassification
# write_db(table, df_drugsclassification, ["PI_ID"])

print
# base = DB_Base()
# base.merge_2_table(
#     result_df,
#     target_table,
#     uniq_keys,
#     where_condition,
#     target_conn)


# In[24]:


# "https://124.172.190.114:8443/api/health/getCiDrugs.json?FIELD=&mdiID=&mdiAtccode=&piID=&mdiSfdaapprovalid=&mdiMedicinename=&mdiUsemethod=&mdiDosform=&mdiSpecificial="
getCiDrugs = "https://124.172.190.114:8443/api/health/getCiDrugs.json"
# key MDI_ID
# params = {
#     "FIELD":"",
#     "piID":"",
#     "piMedicinalname":"",
#     "piBigsortid":""
# }
# ci_drugs = APIVisitor(token, getCiDrugs, username)
# data_drugs = ci_drugs.getcontent({})
# data_drugs

# *****************************************************************
# TODO
df_drugs = access_api(getCiDrugs, params, username, token)
df_drugs_columns = df_drugs.columns
# In[25]:


df_drugs.columns = [u'MDI_ATCCODE', u'MDI_DOSFORM', u'MDI_ID', u'MDI_MEDICINENAME', u'MDI_REMARK1',
                    u'MDI_SFDAAPPROVALID', u'MDI_SPECIFICIAL', u'MDI_USEMETHOD', u'PI_ID']


# df_drugs.head()
# ci_drugs
# write_db(base, "ci_drugs", df_drugs, ["MDI_ID"], where_condition="")

# key_drugs = "MDI_ID"


# # 将API返回的数据转换成df
# df_drugs = pd.DataFrame()
# for i, item in enumerate(data_drugs):
#     df = pd.DataFrame(item, index=[i])
#     df_drugs = df_drugs.append(df)
# df_drugs.info()

# In[19]:


# df_drugs.head()
# # import pandas as pd
# sql = """
# select * from ci_drugs limit where id<10
# """
# data = pd.read_sql(sql, health_conn)
# data.columns


# In[21]:


#
# base.merge_2_table(
#     df_drugs,
#         "ci_drugs",
#         "MDI_ID",
#         "",
#         health_conn)

# In[ ]:


# 整合成一个函数 ，

def getCiDrugssales(params):
    getCiDrugssales = "https://124.172.190.114:8443/api/health/getCiDrugssales.json"
    ci_drugssales = APIVisitor(token, getCiDrugssales, username)
    data_drugssales = ci_drugssales.getcontent(params)

    # 将API返回的数据转换成df
    df_drugssales = pd.DataFrame()
    for i, item in enumerate(data_drugssales):
        df = pd.DataFrame(item, index=[i])
        df_drugssales = df_drugssales.append(df)
    df_drugssales.info()

    # df_drugssales['date'].astype(date)


def format_drugsales(df_drugssales):
    if df_drugssales is None or len(df_drugssales) == 0:
        return None
    df_drugssales['year'] = df_drugssales['date'].apply(lambda x: x[:4])
    df_drugssales['quarter'] = df_drugssales['date'].apply(lambda x: int(x[5:7]) / 3)
    df_drugssales = df_drugssales.drop(['date', 'frequency'], axis=1)
    df_drugssales.head()

    df_drugssales['mdiID'] = df_drugssales['pmdMedicinalinformationid']
    df_drugssales_merge = df_drugssales.merge(
        df_drugs[['mdiID', 'mdiMedicinename', 'mdiUsemethod', 'mdiRemark1', 'mdiDosform', 'mdiSpecificial']],
        on='mdiID', how='left')
    df_drugssales_merge = df_drugssales_merge.drop(["mdiID"], axis=1)

    df_drugssales_merge['piID'] = df_drugssales_merge['pmdMedicinalID']
    df_drugssales_merge = df_drugssales_merge.merge(df_drugsclassification[['piID', 'pmdClass']], on='piID',
                                                    how='left')
    df_drugssales_merge = df_drugssales_merge.drop("piID", axis=1)

    #     df_drugssales_merge.head()
    df_drugssales_merge.columns = [u'PMD_CITY', u'PMD_COMPANYID', u'PMD_COMPANYNAME', u'PMD_MEDICINALID',
                                   u'PMD_MEDICINALINFORMATIONID', u'PMD_MEDICINALSALEMONEY',
                                   u'PMD_MEDICINALSALENUMBER', u'PMD_YEAR', u'PMD_QUARTER', u'PMD_MEDICINALNAME',
                                   u'PMD_USEMETHOD', u'PMD_REMARK1', u'PMD_DOSFORM', u'PMD_SPECIFICIAL', u'PMD_CLASS']

    df_drugssales_merge[u'PMD_DATABASE'] = 1
    return df_drugssales_merge


# In[ ]:
#
#
# import calendar
#
# # 数据的日期为离散值， 为每个季度末。
# report_month = ['03', '06', '09', '12']
# datelist = []
# for year in range(2013, 2020):
#     for mon in report_month:
#         res = calendar.monthrange(year, int(mon))
#         datelist.append("%s-%s-%s" % (str(year), str(mon), str(res[1])))
# # datelist
#
#
# # In[ ]:
# # ***********************************************************************
# # TODO
# # slaes数据需要跟另外两张表中的部分数据进行合并，等到所需字段
# df_drugsclassification.columns = df_drugsclassification_columns
# df_drugs.columns = df_drugs_columns
#
# getCiDrugssales = "https://124.172.190.114:8443/api/health/getCiDrugssales.json"
#
# target_table = "ci_drugssales"
# uniq_keys = ['PMD_YEAR', 'PMD_QUARTER', 'PMD_CITY', 'PMD_MEDICINALINFORMATIONID', 'PMD_COMPANYID']
# # target_conn = DBConn('./config.json').mysql_connection(conn_type='ci_drugssales')
#
# # target_conn = MssqlConn(json.dumps(health_40)).connect()
# # def write_db(base, data, target_table, ):
# #     base.merge_2_table(
# #         data,
# #         target_table,
# #         uniq_keys,
# #         where_condition,
# #         health_conn)
#
# for d in datelist:
#     where_condition = "where pmd_year=%s and pmd_quarter=%s" % (d[0:4], str(int(d.split("-")[1]) / 3))
#
#     params = {
#         "data": d,
#         # "endDate": d,
#     }
#     df = access_api(getCiDrugssales, params, username, token)
#     # dfd = format_drugsales(df)
#
#     write_db(base, target_table, format_drugsales(df), uniq_keys, where_condition)
#     # data = getCiDrugssales(params)
#     # base.merge_2_table(
#     #     data,
#     #     target_table,
#     #     uniq_keys,
#     #     where_condition,
#     #     health_conn)
