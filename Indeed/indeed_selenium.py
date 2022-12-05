from selenium import webdriver
from scrapy import Selector
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from random import randint
import time
from csv import writer


PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

start_url = "https://www.indeed.com/jobs?q=data+engineer&sort=date&fromage=1"
driver.get(start_url)
page_source = driver.page_source
selector = Selector(text=page_source)
links = selector.xpath('//a[contains(@class, "jcs-JobTitle")]/@href').extract()
page_num = 0
amount = 0
for link in links:
    page_num +=1 
    amount +=1
    link = "https://indeed.com" + link
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[page_num])
    driver.get(link)
    time.sleep(randint(1,5))
    link_page = Selector(text=driver.page_source)
    name = link_page.xpath('//h1[contains(@class, "jobsearch-JobInfoHeader")]/text()').extract_first()
    company_name = link_page.xpath('//div[contains(@class, "jobsearch-InlineCompanyRating-companyHeader")]/a/text()').extract_first()
    desc = '\n'.join(link_page.xpath('//div[contains(@id, "jobDescriptionText")]//text()').extract())
    print(name, company_name, desc)
next_page =  selector.xpath('//a[@aria-label="Next Page"]/@href').extract_first()
print(next_page)
while next_page:
    driver.get('https://indeed.com' + next_page)
    sel = Selector(text=driver.page_source)
    links = sel.xpath('//a[contains(@class, "jcs-JobTitle")]/@href').extract()
    page_num = 0
    for link in links:
        page_num +=1 
        link = "https://indeed.com" + link
        driver.get(link)
        amount+=1
        page_desc = Selector(text=driver.page_source)
        time.sleep(randint(1,5))
        name = page_desc.xpath('//h1[contains(@class, "jobsearch-JobInfoHeader")]/text()').extract_first()
        company_name = page_desc.xpath('//div[contains(@class, "jobsearch-InlineCompanyRating-companyHeader")]/a/text()').extract_first()
        desc = '\n'.join(page_desc.xpath('//div[contains(@id, "jobDescriptionText")]//text()').extract())
        print(name, company_name, desc)
    next_page = sel.xpath('//a[@aria-label="Next Page"]/@href').extract_first()
print(amount)
