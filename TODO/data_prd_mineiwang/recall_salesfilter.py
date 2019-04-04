# coding: utf8

import pandas as pd
from common.lib_com import db_base
# from connection import health_conn as target_conn
from data_prd_mineiwang.api_visitor import APIVisitor
from datetime import datetime
import calendar

# from common.logger import logger
from common.config import logger
from common.config import Config

cfg = Config()

target_conn = cfg.health_db.connect()
logger.info("mineiwang salesfilter run")

base = db_base.DB_Base()

# 数据的日期为离散值， 为每个季度末。
# report_month = [3,6,9,12]
report_month = ['03', '06', '09', '12']
datelist = []

this_year = datetime.now().year
for year in range(2013, this_year + 1):
    for mon in report_month:
        res = calendar.monthrange(year, int(mon))
        datelist.append("%s%s%s" % (str(year), str(mon), str(res[1])))
# datelist

# getCiDrugsFilter
username = "rrp"
token = "37468D37D9CE3B7B36749FACF712C245"
urlCiDrugsFilter = "https://124.172.190.114:8443/api/health/getCiDrugsFilter.json?"
apiparams = {
    "FIELD": "",
    "beginDate": "",
    "endDate": "",
    "pmdCity": "",
    "pmdMedicinalinformationid": "",
    "pmdCompanyid": "",
    "pmdCompanyname": "",
    "pmdMedicinalID": "",
}
# API类用于获取数据
ci_getCiDrugsFilter = APIVisitor(token, urlCiDrugsFilter, username, apiparams)


def getCiDrugssalesFiler(params):
    #     getCiDrugssales = "https://124.172.190.114:8443/api/health/getCiDrugssales.json"
    # ci_drugssales = APIVisitor(token, urlCiDrugsFilter, username)
    data = ci_getCiDrugsFilter.getcontent(params)
    if len(data) == 0:
        return None
    # 将API返回的数据转换成df
    data_df = pd.DataFrame(data)
    #     for i,item in enumerate(data_drugssales):
    #         df = pd.DataFrame(item, index=[i])
    #         df_drugssales = df_drugssales.append(df)
    data_df.info()

    #     df_drugssales_merge.head()
    data_df.columns = [u'DATE', u'FREQUENCY', u'PMD_CITY', u'PMD_CLASS', u'PMD_COMPANYID', u'PMD_COMPANYNAME',
                       u'PMD_DOSFORM', u'PMD_MEDICINALID', u'PMD_MEDICINALINFORMATIONID', u'PMD_MEDICINALNAME',
                       u'PMD_REMARK1', u'PMD_SPECIFICIAL', u'PMD_USEMETHOD']
    #
    # PMD_CITY中的“市”去掉
    data_df["PMD_CITY"] = data_df["PMD_CITY"].apply(lambda x: x[:-1] if x.endswith(u'市') else x)
    data_df = data_df.drop_duplicates(subset=uniq_keys, keep='first')
    #     df_drugssales_merge.head()
    return data_df


# slaes数据需要跟另外两张表中的部分数据进行合并，等到所需字段
# df_DrugsFilter.columns = df_drugsclassification_columns
# df_drugs.columns = df_drugs_columns

target_table = "ci_drugs_filter"
uniq_keys = ['DATE', 'PMD_CITY', 'PMD_MEDICINALINFORMATIONID', 'PMD_COMPANYID']


# DATE, PMD_CITY, PMD_MEDICINALINFORMATIONID, PMD_COMPANYID
# PMD_YEAR, PMD_QUARTER, PMD_CITY, PMD_MEDICINALINFORMATIONID, PMD_COMPANYID,PMD_DOSFORM
# target_conn = loader.create_connection(conn_type='ci_drugssales')

def main(datelist):
    for d in datelist:
        where_condition = "where date='%s'" % (d)
        #     d='2015-12-31'
        params = {
            "beginDate": d,
            "endDate": d,
            # "date":d
        }
        logger.info("main run on %s" % d)

        data_df = getCiDrugssalesFiler(params)
        if data_df is not None:
            base.merge_table(
                data_df,
                target_table,
                uniq_keys,
                where_condition,
                target_conn,
                'mysql')


if __name__ == "__main__":
    # datelist = ['20180331']
    # main 由controlm 调度，
    if datetime.now().day == 1:
        # 定时每月1日执行一次全量
        main(reversed(datelist))
    else:
        # 其它时间， 每天执行一次
        main(reversed(datelist[-12:]))

# data_df.columns=[ u'date',u'PMD_COMPANYID',u'PMD_COMPANYNAME',u'PMD_MEDICINALID',u'PMD_MEDICINALINFORMATIONID',u'PMD_MEDICINALSALEMONEY',u'PMD_MEDICINALSALENUMBER',u'PMD_YEAR', u'PMD_QUARTER',u'PMD_REMARK1',u'PMD_DOSFORM',u'PMD_SPECIFICIAL',u'PMD_CLASS']
