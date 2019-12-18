# coding=utf8
from bs4 import BeautifulSoup


class FeedSSE():
    def __init__(self):
        self.url = 'http://www.sse.com.cn/assortment/stock/list/info/company/index.shtml?COMPANY_CODE=%s'

    def get_src_url(self, key):
        return self.url % key

    def get_cn_con(self, soup):
        r = soup.find_all('table', attrs={"class": 'search_'})  # get empty
        r = soup.find_all('div', attrs={"class": 'sse_wrap_cn_con'})
        # id = "tableData_stockListCompany"
        pass

#
# jsonpCallback83052({"actionErrors": [], "actionMessages": [], "errorMessages": [], "errors": {}, "fieldErrors": {},
#                     "isPagination": "false", "jsonCallBack": "jsonpCallback83052", "locale": "zh_CN",
#                     "pageHelp": {"beginPage": 1, "cacheSize": 5, "data": null, "endDate": null, "endPage": null,
#                                  "objectResult": null, "pageCount": null, "pageNo": 1, "pageSize": 10,
#                                  "searchDate": null, "sort": null, "startDate": null, "total": 0}, "result": [
#         {"STATE_CODE_B_DESC": "-", "COMPANY_ABBR": "铁龙物流", "SCU_TYPE": "-", "AREA_NAME_DESC": "辽宁",
#          "COMPANY_ADDRESS": "大连市高新园区火炬路32号创业大厦A座2716号", "LEGAL_REPRESENTATIVE": "吴云天                        ",
#          "ISHLT": "-", "SECURITY_CODE_A_SZ": "-", "SECURITY_CODE_A": "600125", "ENGLISH_ABBR": "CRT",
#          "SECURITY_CODE_B": "-", "IF_VOTE_DIFFERENCE": "-", "STATE_CODE_A_DESC": "上市", "SMALL_CLASS_NAME": "-",
#          "IF_PROFIT": "-", "OTHER_CODE": "-", "SSE_CODE_DESC": "公用事业", "COMPANY_CODE": "600125",
#          "OFFICE_ZIP": "116001", "SECURITY_30_DESC": "否", "FULLNAME": "中铁铁龙集装箱物流股份有限公司",
#          "E_MAIL_ADDRESS": "zhengquan@chinacrt.com", "TYPE": "0", "CSRC_GREAT_CODE_DESC": "铁路运输业",
#          "FOREIGN_LISTING_ADDRESS": "-", "FOREIGN_LISTING_DESC": "否", "CHANGEABLE_BOND_CODE": "-", "OTHER_ABBR": "-",
#          "FULL_NAME_IN_ENGLISH": "CHINA RAILWAY TIELONG CONTAINER LOGISTICS CO., LTD", "CSRC_MIDDLE_CODE_DESC": "-",
#          "SEC_NAME_FULL": "铁龙物流", "WWW_ADDRESS": "www.chinacrt.com", "SECURITY_ABBR_A": "铁龙物流",
#          "CSRC_CODE_DESC": "交通运输、仓储和邮政业", "CHANGEABLE_BOND_ABBR": "-", "OFFICE_ADDRESS": "辽宁省大连市中山区新安街1号",
#          "REPR_PHONE": "-"}], "sqlId": "COMMON_SSE_ZQPZ_GP_GPLB_C", "texts": null, "type": "", "validateCode": ""})

# https://blog.csdn.net/qq_36779888/article/details/79210713