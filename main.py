from selenium import webdriver
from scrapy import Selector
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from random import randint
import requests
import time
from db import create_table, get_engine, get_session, Ads
import csv


driver = webdriver.Chrome(executable_path=r'/home/andrey/Downloads/chromedriver')

SEARCH_QUERIES = ["data+engineer", "terraform", "airflow"]
DOMENS = ["www", "uk"] #, "nl", "de"]

TELEGRAM_TOKEN='5712604269:AAFDrWRqtKcZ1g3EkiIr4i2FeukSdySVGas'
TELEGRAM_CHAT_ID=5592590203

def send_msg(text):
    token = TELEGRAM_TOKEN
    _id = TELEGRAM_CHAT_ID

    url_req = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={_id}&text={text}"
    requests.get(url_req)

def search(query):
    for domen in DOMENS:
        start_url = f"https://{domen}.indeed.com/jobs?q={query}&sc=0kf%3Ajt(contract)%253B&fromage=1"
        parse(start_url)

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
    engine = get_engine()
    create_table(engine)
    session = get_session(engine)
    for link in links:
        link = "https://indeed.com" + link
        driver.get(link)
        time.sleep(randint(1,5))
        link_page = Selector(text=driver.page_source)
        name = link_page.xpath('//h1[contains(@class, "jobsearch-JobInfoHeader")]/text()').extract_first()
        company_name = link_page.xpath('//div[contains(@class, "jobsearch-InlineCompanyRating-companyHeader")]/a/text()').extract_first()
        desc = '\n'.join(link_page.xpath('//div[contains(@id, "jobDescriptionText")]//text()').extract())
        # send_msg(f"{name}, {company_name}, {desc}, {link}")
        new_ad = Ads(title=name, company=company_name, description=desc, link=link)
        choose = session.query(Ads).filter(Ads.link == link).first()
        if choose:
            continue

        session.add(new_ad)

        session.commit()
        print(name, company_name, desc)
        session.close()

def main():
    for query in SEARCH_QUERIES:
        search(query)

main()
