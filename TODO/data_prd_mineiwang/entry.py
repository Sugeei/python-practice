# coding: utf8

from data_prd_mineiwang.recall_salesfilter import main
from data_prd_mineiwang.recall_salesfilter import datelist

if __name__ == "__main__":
    # 此入口函数用于刷全量数据
    main(reversed(datelist))

    # Todo log is not ready
