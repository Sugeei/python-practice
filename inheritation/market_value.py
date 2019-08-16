# coding=utf8
from inheritation.stylecalculator import StyleCalculator


class MarketValue(StyleCalculator):
    def __init__(self):
        self.stylename = 'market_value_style'

    def data_init(self, config, dateitem):
        """from where to get source data"""
        """NegMktValue"""
        sql = """select exchange_cd, ticker_symbol, trade_date, neg_market_value 
        from mkt_equd where 
        trade_date='%s'""" % dateitem
        conn = config.datayesdb_ro
        return conn, sql
    #
    # def write(self):
    #     """to database"""
    #
    #     """
    #     uniqkeys 应该是columns名称被修改之后的
    #     """
    #     target_table = "stock_factor_tags"
    #     uniqkeys = ['ticker', 'trade_date']
    #     print(self.stylename, " inherited")
    #     # return config.datayesdb_rw, target_table, uniqkeys, self.stylename, """where trade_date=%s""" % \
    #     #        dateitem.replace('-', '')

    def run(self, datadf):
        """
        the calculation steps are in the base class
        :param data:
        :return:
        """
        # df = self.style("REVENUE", [0.1, 0.3, 0.5], ['小盘', '中盘', '大盘', '超级大盘'])
        # df= pd.

        datadf.loc[:, 'security_id'] = datadf['ticker_symbol'] + '.' + datadf['exchange_cd']
        datadf.loc[:, 'trade_date'] = datadf['trade_date'].apply(lambda x: x.replace('-', ''))
        df = self.percentage(datadf, "neg_market_value", [0.1, 0.3, 0.5], ['小盘', '中盘', '大盘', '超级大盘'])
        df = df[['ticker_symbol', 'trade_date', 'security_id', 'neg_market_value']]
        df.columns = ['ticker', 'trade_date', 'security_id', 'market_value_style']
        return df
