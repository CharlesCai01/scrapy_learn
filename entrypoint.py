from scrapy.cmdline import execute
execute(['scrapy', 'crawl', 'tutor','-o','tutor.csv','-t','csv'])