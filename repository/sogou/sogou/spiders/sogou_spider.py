import scrapy
from sogou.items import SogouItem
from scrapy.shell import inspect_response

class sogou_spider(scrapy.Spider):
    name = "sogou"
    start_urls = [
        "http://weixin.sogou.com/"
    ]

    def parse(self,response):
        dataList = response.xpath("//*[@id='pc_0_d']")
        items = []
        # 下面的代码调试用
        inspect_response(response, self)  # Rest of parsing code.
        for index,data in enumerate(dataList):
            title = data.xpath('.//div[@class="txt-box"]/h3/a/text()').extract_first()
            brief_text = data.xpath('.//div[@class="txt-box"]/p/text()').extract_first()
            author = data.xpath('.//div[@class="s-p"]/a/text()').extract_first()
            time = data.xpath('.//div[@class="s-p"]/span/text()').extract_first()
            #
            # print "title"+title
            # print "content introduction"+brief_text
            # print "author"+author
            # print "published time"+time
            # print "\n"

            try:
                item = SogouItem()
                item['title'] = title
                item['brief_text'] = brief_text
                item['author'] = author
                item['time'] = time
                items.append(item)
            except:
                pass
        print(items)
        return items

