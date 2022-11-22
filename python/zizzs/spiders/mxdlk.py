import scrapy
from zizzs.items import ZizzsItem
from scrapy.linkextractors import LinkExtractor
from scrapy import Request


class MxdlkSpider(scrapy.Spider):
    name = 'mxdlk'
    allowed_domains = ['zizzs.com']
    #start_urls = ['http://zizzs.com/']
    start_urls = ['https://www.zizzs.com/c/202207/76221.html']
    base_domain = "https://www.zizzs.com"
    pattern = "https://www.zizzs.com/c/"
    def __init__(self):
        self.link_extractor = LinkExtractor(restrict_xpaths = ['//*[@id="content"]/table'])
    

    def parse(self, response: scrapy.http.Response):
        for link in self.link_extractor.extract_links(response):
            if self.pattern in link.url:
                print(link)
                yield ZizzsItem(name = link.text, url = link.url)

