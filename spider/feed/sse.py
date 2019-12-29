# coding=utf8
from bs4 import BeautifulSoup
from feed.abstract import FeedBase
from config.logger import logger


class FeedSSE(FeedBase):
    def __str__(self):
        return u"上海证券交易所"

    def __init__(self):
        self.shortname = 'sse_listed_info'
        self.url = 'http://www.sse.com.cn/assortment/stock/list/info/company/index.shtml?COMPANY_CODE=%s'

    def get_src_url(self, key):
        # logger.info("valid url=%s" % (self.url % key))
        return self.url % key

    def get_cn_con(self, soup):
        res = []
        r = soup.find_all('table')  # get empty
        for item in r:
            th = item.find_all('th')
            td = item.find_all('td')
            for h, d in zip(th, td):
                # print(h.text, d.text)
                res.append([h.text, d.text])
        # logger.info("valid data length=%s" % (len(res)))
        return res
        #
        # # r = soup.find_all('div', attrs={"class": 'overview-slide'})
        # r = soup.find_all('div', attrs={"id": 'tableData_stockListCompany'})
        # r = soup.find_all('div', attrs={"class": 'sse_wrap_cn_con'})
        # for item in soup.find_all('div', attrs={"class": 'sse_wrap_cn_con'}):
        #     if item.find('div', attrs={"id": 'tableData_stockListCompany'}):
        #         s = item.find('table')
        #     print(item)
        # s = r[1].find('table')
        # # id = "tableData_stockListCompany"
        # print(r)
        pass

    def save_local_file(self, content):
        with open('%s.txt', 'a') as f:
            f.write(content)
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
            # < !--一级内容 -->
            # < div
            #
            # class ="sse_wrap_cn_con" > < div class ="tab-pane active js_tableT05" id="tableData_stockListCompany" >
            #
            # < div
            #
            # class ="sse_table_title2" > < p > < / p > < / div >
            #
            # < div
            #
            # class ="table-responsive sse_table_T05" > < table class ="table search_" > < tbody > < tr > < th > 公司代码 < / th > < td > 600125 < / td > < / tr > < tr > < th > 股票代码 * < / th > < td > 600125 / - / - < / td > < / tr > < tr > < th > 上市日 * < / th > < td > < a href="/assortment/stock/list/info/financing/index.shtml?COMPANY_CODE=600125" target="_blank" > 1998-05-11 < / a > / - / - < / td > < / tr > < tr > < th > 可转债简称（代码） / < br / > 可转债转股简称（代码） < / th > < td > -(-) / -(-) < / td > < / tr > < tr > < th > 公司简称(中 / 英) < / th > < td > 铁龙物流 / CRT < / td > < / tr > < tr > < th > 公司全称(中 / 英) < / th > < td > 中铁铁龙集装箱物流股份有限公司 / CHINA RAILWAY TIELONG CONTAINER LOGISTICS CO., LTD < / td > < / tr > < tr > < th > 注册地址 < / th > < td > 大连市高新园区火炬路32号创业大厦A座2716号 < / td > < / tr > < tr > < th > 通讯地址（邮编） < / th > < td > 辽宁省大连市中山区新安街1号(116001) < / td > < / tr > < tr > < th > 法定代表人 < / th > < td > 吴云天 < / td > < / tr > < tr > < th > 董事会秘书姓名 < / th > < td > 畅晓东 < / td > < / tr > < tr > < th > E-mail < / th > < td > < a href="mailto:zhengquan@chinacrt.com" target="_blank" > zhengquan @ chinacrt.com < / a > < / td > < / tr > < tr > < th > 联系电话 < / th > < td > - < / td > < / tr > < tr > < th > 网址 < / th > < td > < a href="http://www.chinacrt.com" target="_blank" > http://
            #
            #     www.chinacrt.com < / a > < / td > < / tr > < tr > < th > CSRC行业(
            #     门类 / 大类 / 中类) < / th > < td > 交通运输、仓储和邮政业 / 铁路运输业 / - < / td > < / tr > < tr > < th > SSE行业 < / th > < td > 公用事业 < / td > < / tr > < tr > < th > 所属省 / 直辖市 < / th > < td > 辽宁 < / td > < / tr > < tr > < th > 状态 * < / th > < td > 上市 / - / - < / td > < / tr > < tr > < th > 是否上证180样本股 < / th > < td > 否 < / td > < / tr > < tr > < th > 是否境外上市 < / th > < td > 否 < / td > < / tr > < tr > < th > 境外上市地 < / th > < td > - < / td > < / tr > < / tbody > < / table > < / div >
            # < div
            #
            # class ="sse_table_conment" > < p > 注： * 代表A股 / B股 / CDR < / p > < / div >
            #
            # < / div >
            # < / div >
            # < !--一级内容结束 -->一级内容结束

            # https://blog.csdn.net/qq_36779888/article/details/79210713
