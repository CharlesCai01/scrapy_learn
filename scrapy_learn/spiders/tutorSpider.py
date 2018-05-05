# -*- coding:UTF-8 -*-
import scrapy
from scrapy_learn.items import TutorItem
from scrapy_learn.filterTags import filter_tags



class TutorSpider(scrapy.Spider):
    name = 'tutor'
    allowed_domains = ['ggglxy.scu.edu.cn']
    start_urls=['http://ggglxy.scu.edu.cn/index.php?c=article&a=type&tid=18']
    # 初始化item对象保存爬取的信息
    item = TutorItem()
    
    def parse(self,response):
        for tutor in response.xpath("//li[@class='fl']"):
            # 爬取姓名，职称，专业，邮箱
            item = TutorItem()
            item['image_urls'] = {"http://ggglxy.scu.edu.cn"+tutor.xpath("div[@class='l fl']/a/img/@src").extract_first()}
            item['name'] = tutor.xpath("div[@class='r fr']/h3[@class='mb10']/text()").extract_first()
            item['position'] = tutor.xpath("div[@class='r fr']/p[@class='color_main f14']/text()").extract_first()
            item['major'] = tutor.xpath("div[@class='r fr']/div[@class='desc']/p[1]/text()").extract_first()
            item['email'] = tutor.xpath("div[@class='r fr']/div[@class='desc']/p[2]/text()").extract_first()
             
            # 获取详情页的地址并传送给单个页面处理函数进行处理 -> parse_details()
            href = tutor.xpath("div[@class='l fl']/a/@href").extract_first()
            url = response.urljoin(href)
            request = scrapy.Request(url,callback=self.parse_details)
            request.meta['item'] = item
            yield request

        ## 是否还有下一页，如果有的话，则继续
        next_page=response.xpath("//div[@class='pager cf tc pt10 pb10 mobile_dn']/li[last()-1]/a/@href").extract_first()
        if next_page is not None:
            next_pages = response.urljoin(next_page)
            ## 将 「下一页」的链接传递给自身，并重新分析
            yield scrapy.Request(next_pages, callback = self.parse)

    # 编写详情页爬取方法
    def parse_details(self, response):
        item = response.meta['item']
        item['description'] = response.xpath("//div[@class='r fr']/div/text()").extract_first()
        item['researchResult'] = filter_tags(response.xpath("//div[@class='right_info p20']/div[2]").extract_first())
        item['award'] = filter_tags(response.xpath("//div[@class='right_info p20']/div[3]").extract_first())
        item['sciResearPro'] = filter_tags(response.xpath("//div[@class='right_info p20']/div[4]").extract_first())
        item['talentTrain'] = filter_tags(response.xpath("//div[@class='right_info p20']/div[5]").extract_first())
        yield item