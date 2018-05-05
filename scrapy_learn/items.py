# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field() #姓名
    position = scrapy.Field() #职称
    major = scrapy.Field() #专业
    email = scrapy.Field() #邮箱
    description = scrapy.Field()  #简介
    researchResult = scrapy.Field() #代表性研究成果
    award = scrapy.Field() #获奖情况
    sciResearPro = scrapy.Field() #科研项目
    talentTrain = scrapy.Field() #人才培养