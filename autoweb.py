from selenium import webdriver
from threading import Thread
import time
from selenium.webdriver.common.by import By


prefs = prefs = {
'download.prompt_for_download': False,
'download.extensions_to_open': 'rpm',
'safebrowsing.enabled': True
}
opts = webdriver.ChromeOptions()
opts.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_options=opts, executable_path='../chromedriver')

driver = webdriver.Chrome('../chromedriver')
driver.get('https://developer.aliyun.com/packageSearch')

try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "search")))
finally:
    driver.find_element(By.CLASS_NAME, 'search').click()
    driver.find_element(By.CLASS_NAME, 'search').send_keys(
        "libnuma1 2.0.12-1+b1")
    driver.find_element(By.CLASS_NAME, 'search').send_keys(Keys.ENTER)
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'btn')))
# finally:
finally:
    driver.find_element(By.CLASS_NAME, 'btn').click()
    driver.find_element(
        By.XPATH, '//*[@id="mirror-search"]/div/div[3]/div[1]/div[2]/div[1]/div[5]/a').click()
    print('success')

time.sleep(20)
