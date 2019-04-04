import json
import pymysql
import pymssql


# from common.config import Config


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


health_40 = {"server": "db-mssql02.datayes-stg.com", "port": 1433, "database": "health", "user": "talend_load",
             "password": "s9t5gNThn2vqWM7c", "charset": "utf8"}

# bigdata_conn = MysqlConn(json.dumps(bigdata)).connect()
# dateyesdbp_conn = MysqlConn(json.dumps(dateyesdbp)).connect()

health_conn = MssqlConn(json.dumps(health_40)).connect()
