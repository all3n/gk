import scrapy
import os
import json
from scrapy.linkextractors import LinkExtractor
import requests



def download_file(url, local_filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)

class SummarySpider(scrapy.Spider):
    name = 'summary'
    allowed_domains = ['zizzs.com']
    start_urls = ['http://zizzs.com/']
    st_title = ['科目', '试题', '答案']

    pattern = "https://www.zizzs.com/c/"
    base_url = "https://www.zizzs.com"
    def __init__(self):
        self.link_extractor = LinkExtractor(restrict_xpaths = ['//*[@id="content"]/table'])

    def start_requests(self):
        with open("url.json", "r", encoding='utf-8') as f:
            jl = json.loads(f.read())
            for info in jl:
                yield scrapy.Request(url=info["url"], callback=self.parse, meta = {"name": info['name'], 'category': 1, 'url': info['url']})


    def parse(self, response):
        print(response.meta)
        name = response.meta['name']
        category = response.meta['category']
        if category == 1:
            for link in self.link_extractor.extract_links(response):
                print(link)
                yield scrapy.Request(url=link.url, callback=self.parse, meta = {"name": name, 'category': 2, 'url': link.url})
        elif category == 2:
            output = os.path.join('data', name)
            download = response.css('a.download')
            for d in download:
                t = d.xpath('u/text()').extract()[0]
                d_path = os.path.join(output, t + ".pdf")
                d_url = d.attrib['href']
                if self.base_url not in d_url:
                    d_url = self.base_url + d_url
                if not os.path.exists(d_path):
                    if not os.path.exists(output):
                        os.makedirs(output)
                    download_file(d_url, d_path)
