# coding: utf8

# In[1]:

# from lib.config import Config, logger
# from utils import data_api_prefix

from api_visitor import access_api
from config import getCiDrugsclassification, getCiDrugs, getCiDrugssales
from config import username, token, health_conn
from db_base import write_db
from logger import logger

# key:PI＿ID
params = {
    "FIELD": "",
    "piID": "",
    "piMedicinalname": "",
    "piBigsortid": ""
}

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
write_db(health_conn, table, df_drugsclassification, ["PI_ID"])


# *****************************************************************
# TODO
df_drugs = access_api(getCiDrugs, params, username, token)
df_drugs_columns = df_drugs.columns
# In[25]:
df_drugs.columns = [u'MDI_ATCCODE', u'MDI_DOSFORM', u'MDI_ID', u'MDI_MEDICINENAME', u'MDI_REMARK1',
                    u'MDI_SFDAAPPROVALID', u'MDI_SPECIFICIAL', u'MDI_USEMETHOD', u'PI_ID']


# df_drugs.head()
# ci_drugs
write_db(health_conn, "ci_drugs", df_drugs, ["MDI_ID"], where_condition="")


# key_drugs = "MDI_ID"


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


import calendar

# 数据的日期为离散值， 为每个季度末。
report_month = ['03', '06', '09', '12']
datelist = []
for year in range(2013, 2020):
    for mon in report_month:
        res = calendar.monthrange(year, int(mon))
        datelist.append("%s-%s-%s" % (str(year), str(mon), str(res[1])))
# datelist
#
# In[ ]:
# ***********************************************************************
# TODO
# slaes数据需要跟另外两张表中的部分数据进行合并，等到所需字段
df_drugsclassification.columns = df_drugsclassification_columns
df_drugs.columns = df_drugs_columns

target_table = "ci_drugssales"
uniq_keys = ['PMD_YEAR', 'PMD_QUARTER', 'PMD_CITY', 'PMD_MEDICINALINFORMATIONID', 'PMD_COMPANYID',
             'PMD_MEDICINALSALENUMBER']
# target_conn = DBConn('./config.json').m

for d in reversed(datelist):
    where_condition = "where pmd_year=%s and pmd_quarter=%s" % (d[0:4], str(int(d.split("-")[1]) / 3))

    params = {
        "beginDate": d,
        "endDate": d,
    }
    logger.info("work on ci_drugssales %s" % d)
    df = access_api(getCiDrugssales, params, username, token)
    # dfd = format_drugsales(df)
    write_db(health_conn, target_table, format_drugsales(df), uniq_keys, where_condition)
    # data = getCiDrugssales(params)
