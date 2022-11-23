from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Chrome("/usr/bin/google-chrome")
driver.get("https://www.indeed.com")
driver.close()