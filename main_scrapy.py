from datetime import datetime

import scrapy
from scrapy import Request, Item, Field
from scrapy.spiders import Spider
from scrapy.crawler import CrawlerProcess
import csv
from scrapy.utils.response import open_in_browser

class RowItem(Item):
    name = Field()
    company_name = Field()
    desc = Field()
    link = Field()


class PricePipeline:
    def process_item(self, item, spider):
        return item

SEARCH_QUERIES = ["data engineer", "terraform", "python"]

class FindJobsSpider(Spider):
    name = 'findjobs'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}
    custom_settings = {
        'ITEM_PIPELINES': {
            'main.PricePipeline': 300
        }, 
        "FEEDS": {
            'items.csv': {
                'fields': ['name', 'company_name', 'desc', 'link'],
                'format': 'csv',
            },
        }
    }

    # def __init__(self, latest_id='%%%', *args, **kwargs):
    #     super().__init__(self, *args, **kwargs)
    #     self.latest_id = latest_id
    #     print(latest_id)

    def start_requests(self):
        yield Request(url = "https://www.indeed.com/jobs?q=data&l=&from=searchOnHP", callback=self.parse)

    def parse(self, response):
        for link in response.xpath('//a[contains(@class, "jcs-JobTitle")]/@href').extract():
            url = response.urljoin(link)
            # if self.latest_id in url:date
            #     print('*'*88, f"stopping on {url}")
            #     return
            yield Request(url, callback=self.parse_details)


        page = response.xpath('//a[@aria-label="Next Page"]/@href').extract_first()
        if page:
            yield Request(response.urljoin(page), callback=self.parse)

    def parse_details(self, response):
        name = response.xpath('//h1[contains(@class, "jobsearch-JobInfoHeader")]/text()').extract_first()
        company_name = response.xpath('//div[contains(@class, "jobsearch-InlineCompanyRating-companyHeader")]/a/text()').extract_first()
        # date = response.xpath('//div[contains(@class, "jobsearch-JobMetadataFooter")]/div[2]/text()').extract_first()
        desc = '\n'.join(response.xpath('//div[contains(@id, "jobDescriptionText")]//text()').extract())
        link = response.url
        yield RowItem(name=name,
                      company_name=company_name,
                      desc=desc,
                      link=link
                    )

def main():
    from pathlib import Path

    my_file = Path("items.csv")
    latest_id = '###'
    # if my_file.is_file():
    #     with open('items.csv', 'r') as f:
    #         reader = csv.reader(f)
    #         rows = [row for row in reader]
    #         f.close()
    #         latest_id = rows[-1][3].split('jk=')[1].split('&')[0]


    process = CrawlerProcess(settings={
    "FEEDS": {
        "items.csv": {"format": "csv"},
    }})
    process.crawl(FindJobsSpider, latest_id=latest_id)
    process.start()

if __name__ == '__main__':
    main()
