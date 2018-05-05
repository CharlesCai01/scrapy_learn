# -*- coding:UTF-8 -*-
import scrapy
from scrapy_learn.items import TutorItem



class TutorSpider(scrapy.Spider):
    name = 'tutor'
    allowed_domains = ['ggglxy.scu.edu.cn']
    start_urls=['http://ggglxy.scu.edu.cn/index.php?c=article&a=type&tid=18']
    
    def parse(self,response):
        for href in response.xpath("//div[@class='l fl']/a/@href"):
            url = response.urljoin(href.extract())
            ## 将得到的页面地址传送给单个页面处理函数进行处理 -> parse_details()
            yield scrapy.Request(url,callback=self.parse_details)

            ## 是否还有下一页，如果有的话，则继续
            next_page=response.xpath("//div[@class='pager cf tc pt10 pb10 mobile_dn']/li[last()-1]/a/@href").extract_first()

            if next_page is not None:
                next_pages = response.urljoin(next_page)
                ## 将 「下一页」的链接传递给自身，并重新分析
                yield scrapy.Request(next_pages, callback = self.parse)

# 编写爬取方法
    def parse_details(self, response):
        #for line in response.xpath("//ul[@class='newsinfo_list_ul mobile_dn']"):
        # 初始化item对象保存爬取的信息
        item = TutorItem()
        # 这部分是爬取部分，使用xpath的方式选择信息，具体方法根据网页结构而定
        item['name'] = response.xpath("//div[@class='r fr']/h3/text()").extract()
        item['position'] = response.xpath("//div[@class='r fr']/p/text()").extract()
        item['description'] = response.xpath("//div[@class='r fr']/div/text()").extract()
        yield item