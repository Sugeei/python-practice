# coding=utf8
import math


class StyleCalculator():
    def __init__(self):
        pass
        # self.stylename = style
        # self.dataloader = dataloader
        # self.datawriter = datawriter

    def tag_range(self, percentile, tags):
        """
        计算出每个标签对应的取值范围ss
        :return:
        """
        if not len(percentile) + 1 == len(tags):
            raise ValueError
        tagrange = []
        tagrange.append((0, percentile[0]))
        for i in range(len(percentile) - 1):
            tagrange.append((percentile[i], percentile[i + 1]))
        try:
            tagrange.append((percentile[-1], math.inf))
        except:
            tagrange.append((percentile[-1], float('inf')))

        return tagrange

    def percentage(self, datadf, targetcol, percentile, tags):
        """
        classify by percentage
        :param datadf:
        :param targetcol: target column name
        :param percentage: [0.3, 0.4, 0.9]
        :param tags: should have same length with len(percentage)+1
        :return:
        """
        if len(datadf) == 0:
            return datadf
        print(percentile)
        # sortdf = datadf.sort_values(by=[targetcol], ascending=ascending)
        separator = []
        for p in percentile:
            separator.append(int(datadf[targetcol].quantile(p)))
        tagrange = self.tag_range(separator, tags)

        # datadf[targetcol + '_style'] = datadf[targetcol]

        def stylemap(val):
            for i, v in enumerate(tagrange):
                if val >= v[0] and val < v[1]:
                    return tags[i]

        datadf[targetcol] = datadf[targetcol].apply(stylemap)
        # datadf[targetcol + '_style'] = datadf[targetcol + '_style'].apply(stylemap)
        return datadf

    def write(self):
        """to database"""
        """
        uniqkeys 应该是columns名称被修改之后的
        """
        target_table = "stock_factor_tags"
        uniqkeys = ['ticker', 'trade_date']
        print(self.stylename)
        # return config.datayesdb_rw, target_table, uniqkeys, self.stylename, """where trade_date=%s""" % \
        #        dateitem.replace('-', '')
