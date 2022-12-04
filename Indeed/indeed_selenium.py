from selenium import webdriver
from scrapy import Selector
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from csv import writer


PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

start_url = "https://www.indeed.com/jobs?q=data+engineer"
driver.get(start_url)
page_source = driver.page_source
selector = Selector(text=page_source)
links = selector.xpath('//a[contains(@class, "jcs-JobTitle")]/@href').extract()
page_num = 0
for link in links:
    page_num +=1 
    link = "https://indeed.com" + link
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(link)
    link_page = Selector(text=driver.page_source)
    name = link_page.xpath('//h1[contains(@class, "jobsearch-JobInfoHeader")]/text()').extract_first()
    company_name = link_page.xpath('//div[contains(@class, "jobsearch-InlineCompanyRating-companyHeader")]/a/text()').extract_first()
    desc = '\n'.join(link_page.xpath('//div[contains(@id, "jobDescriptionText")]//text()').extract())
    print(name, company_name, desc)
