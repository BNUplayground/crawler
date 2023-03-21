from selenium import webdriver
import time
from selenium.webdriver.common.by import By


opts = webdriver.ChromeOptions()
driver = webdriver.Chrome(chrome_options=opts, executable_path='../chromedriver')

driver = webdriver.Chrome('../chromedriver')
driver.get('https://developer.aliyun.com/packageSearch')
driver.find_element(By.CLASS_NAME, 'search').click()
driver.find_element(By.CLASS_NAME, 'search').send_keys("sqlite-libs")
driver.find_element(By.CLASS_NAME, 'btn').click()
driver.find_element(By.XPATH, '//*[@id="mirror-search"]/div/div[3]/div[1]/div[2]/div[1]/div[5]/a').click()