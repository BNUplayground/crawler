from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Define the preferences for Chrome
prefs = {
    'download.prompt_for_download': False,
    'download.extensions_to_open': 'deb',
    'safebrowsing.enabled': True
}

# Set up Chrome options with the preferences
opts = webdriver.ChromeOptions()
opts.add_experimental_option("prefs", prefs)
opts.add_experimental_option('excludeSwitches', ['enable-logging'])
# Initialize the Chrome driver with the options and executable path
driver = webdriver.Chrome(options=opts, executable_path='../chromedriver')
driver.implicitly_wait(10)
# Navigate to the target website
# driver.get('https://developer.aliyun.com/packageSearch')


def search_and_download_package(package_name):
    driver.get('https://developer.aliyun.com/packageSearch')
    key = driver.find_element(By.CLASS_NAME, 'search')  # get input box
    key.send_keys(package_name)  # send search context
    search = driver.find_element(By.CLASS_NAME, 'btn')  # get button
    search.click()  # click search button
    # get download button
    time.sleep(2)
    download = driver.find_element(By.LINK_TEXT, '下载')
    download.click()
    # key.clear()
    # print(key)

    time.sleep(2)
    # key2 = driver.find_element(By.CLASS_NAME, 'item-name')  # get input box
    # print(key2.get_attribute('href'))
    links = driver.find_elements(By.XPATH,
                                 '//*[@id="mirror-search"]/div/div[3]/div[1]/div[2]/div[1]/div[1]/a')
    print(links[0].get_attribute('href'))
    # a=link.get_attribute('href')
    # print(a)
    # key2.click()
    driver.get(links[0].get_attribute('href'))
    # driver.find_element()
    try:
        # 查找 requires 和 provides 标签
        requires_h2 = driver.find_element(By.XPATH, '//h2[text()="requires"]')
        provides_h2 = driver.find_element(By.XPATH, '//h2[text()="provides"]')

        # 提取 requires 和 provides 之间的所有 <p> 标签
        paragraphs = driver.find_elements(By.XPATH,
                                          '//h2[text()="requires"]/following-sibling::p[following-sibling::h2[text()="provides"]]')
        # print(paragraphs)
        # print(paragraphs[0].text)
        # 打印提取到的 <p> 标签内容
        print("在 <h2> requires </h2> 和 <h2> provides </h2> 之间的 <p> 标签内容：")
        for p in paragraphs:
            print(p.text)

        # get package url

    except Exception:
        print("未找到指定的 <h2> 标签。")

    path = driver.find_element(By.XPATH, '//p[contains(text(), "path")]')
    span_element = path.find_element(By.XPATH, './span')
    path_text = span_element.text
    print(f'path: {path_text}')


search_and_download_package("libnuma1 2.0.12-1+b1")
time.sleep(5)
search_and_download_package("liblsan0 8.3.0-6")
