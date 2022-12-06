from selenium import webdriver
from scrapy import Selector
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from random import randint
import time
from csv import writer


PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
SEARCH_QUERIES = ["data+engineer", "terraform"]
start_url = "https://www.indeed.com/jobs?q=data+engineer&sc=0kf%3Ajt%28contract%29%3B&sort=date&fromage=1&vjk=607b75599f92b916"

def parse(link):
    driver.get(link)
    page_source = driver.page_source
    selector = Selector(text=page_source)
    links = selector.xpath('//a[contains(@class, "jcs-JobTitle")]/@href').extract()
    next_page =  selector.xpath('//a[@aria-label="Next Page"]/@href').extract_first()
    parse_details(links)
    if next_page:
        next_page = "https://indeed.com" + next_page
        parse(next_page)

def parse_details(links):
    page_num = 0
    for link in links:
        link = "https://indeed.com" + link
        page_num +=1
        driver.get(link)
        time.sleep(randint(1,5))
        link_page = Selector(text=driver.page_source)
        name = link_page.xpath('//h1[contains(@class, "jobsearch-JobInfoHeader")]/text()').extract_first()
        company_name = link_page.xpath('//div[contains(@class, "jobsearch-InlineCompanyRating-companyHeader")]/a/text()').extract_first()
        desc = '\n'.join(link_page.xpath('//div[contains(@id, "jobDescriptionText")]//text()').extract())
        print(name, company_name, desc)

def main():
    parse(start_url)

main()
