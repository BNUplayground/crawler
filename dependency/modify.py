from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import re
import time
# import csv
import json

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
driver = webdriver.Chrome(
    options=opts, executable_path='../chromedriver')
driver.implicitly_wait(10)

# open a file to record the result
# f = open('package_result.json', 'a+')
# json_writer = json.writer(f)

import re

def extract_package_name(package_name):
    pattern = r"(\w+)\s"
    match = re.match(pattern, package_name)
    if match:
        return match.group(1)
    else:
        return None

#package_name = "liblsan0 8.3.0-6"

#print(f"Extracted package name: {extracted_package_name}")




def search_and_download_package(package_name):
    driver.get('https://developer.aliyun.com/packageSearch')
    time.sleep(1)

    key = driver.find_element(By.CLASS_NAME, 'search')  # get input box
    key.send_keys(package_name)  # send search context
    search = driver.find_element(By.CLASS_NAME, 'btn')  # get button
    search.click()  # click search button

    # download operation
    time.sleep(2)
    # download = driver.find_element(By.LINK_TEXT, '下载')
    # download.click()

    # time.sleep(2)

    #links = driver.find_elements(By.XPATH,
    #                             '//*[@id="mirror-search"]/div/div[3]/div[1]/div[2]/div[1]/div[1]/a')

    extracted_package_name = extract_package_name(package_name)
    print(extracted_package_name)
    item_type_element = driver.find_element_by_xpath(f"//div[text()='{extracted_package_name}']")
    print(item_type_element)
    item_name_element = item_type_element.find_element_by_xpath("./preceding-sibling::div/a")
    href = item_name_element.get_attribute('href')
    website = str(href)
    driver.get(href)
    # print(website)
    #driver.get(links[0].get_attribute('href'))
    try:
        # 提取 requires 和 provides 之间的所有 <p> 标签
        paragraphs = driver.find_elements(By.XPATH,
                                          '//h2[text()="requires"]/following-sibling::p[following-sibling::h2[text()="provides"]]')

        # 打印提取到的 <p> 标签内容
        print("在 <h2> requires </h2> 和 <h2> provides </h2> 之间的 <p> 标签内容：")
        require = []
        for p in paragraphs:
            # print(p.text)
            p = str(p.text)
            req_name, req_version = p.split(' ', 1)
            print(req_name, req_version)
            required_package_size, require_package_path = search_required_package_information(
                req_name, req_version)
            result = {
                'required_package_name': req_name,
                'required_version': req_version,
                'required_package_size': required_package_size,
                'required_package_path': require_package_path
            }
            require.append(result)
        print(require)

        # get package url

    except Exception:
        print("未找到指定的 <h2> 标签。")

    path = driver.find_element(By.XPATH, '//p[contains(text(), "path")]')
    span_element = path.find_element(By.XPATH, './span')
    path_text = span_element.text
    print(f'path: {path_text}')

    # get package size
    url = f" http://mirrors.163.com/{path_text}"
    response = requests.head(url)
    content_length = int(response.headers.get("Content-Length", 0))

    data = {
        "package_name": package_name,
        "package_size": content_length,
        "website": website,
        "path": path_text,
        "requires": require,

    }
    print(data)
    with open("package_result.json", "a+") as f:
        json_str = json.dumps(data)
        f.write(json_str)
        f.write(",\n")


def search_required_package_information(package_name, package_version):
    package_version = re.sub(r"^\D+|\D+$", "", package_version)
    driver.execute_script("window.open('about:blank', '_blank');")
    driver.switch_to.window(driver.window_handles[-1])
    driver.get('https://developer.aliyun.com/packageSearch')
    key = driver.find_element(By.CLASS_NAME, 'search')  # get input box
    key.send_keys(package_name, ' ', package_version)  # send search context
    search = driver.find_element(By.CLASS_NAME, 'btn')  # get button
    search.click()  # click search button
    time.sleep(2)
    links = driver.find_elements(By.XPATH,
                                 '//*[@id="mirror-search"]/div/div[3]/div[1]/div[2]/div[1]/div[1]/a')
    driver.get(links[0].get_attribute('href'))
    path = driver.find_element(By.XPATH, '//p[contains(text(), "path")]')
    span_element = path.find_element(By.XPATH, './span')
    path_text = span_element.text
    url = f" http://mirrors.163.com/{path_text}"
    response = requests.head(url)
    content_length = int(response.headers.get("Content-Length", 0))
    print(content_length)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    return content_length, path_text


# search_and_download_package("libnuma1 2.0.12-1+b1")
search_and_download_package("liblsan0 8.3.0-6")
time.sleep(5)