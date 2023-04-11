from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import re
import time

prefs = {
    'download.prompt_for_download': False,
    'download.extensions_to_open': 'deb',
    'safebrowsing.enabled': True
}

opts = webdriver.ChromeOptions()
opts.add_experimental_option("prefs", prefs)
opts.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(
    options=opts, executable_path='chromedriver')
driver.implicitly_wait(10)

def get_package_information(package_name,OriginalVersion,FixedVersion):
    driver.get('https://developer.aliyun.com/packageSearch')
    time.sleep(1)

    key = driver.find_element(By.CLASS_NAME, 'search')  # get input box
    key.send_keys(package_name)  # send search context
    search = driver.find_element(By.CLASS_NAME, 'btn')  # get button
    search.click()
    time.sleep(2)

    search_name = package_name.split(' ')[0]
    print(search_name)
    item_type_element = driver.find_element(By.XPATH,f"//div[text()='{search_name}']")
    print(item_type_element)
    item_name_element = item_type_element.find_element(By.XPATH,"./preceding-sibling::div/a")
    href = item_name_element.get_attribute('href')
    website = str(href)
    driver.get(href)

    try:
    # 提取 requires 和 provides 之间的所有 <p> 标签
        paragraphs = driver.find_elements(By.XPATH,
                                        '//h2[text()="requires"]/following-sibling::p[following-sibling::h2[text()="provides"]]')

        # 打印提取到的 <p> 标签内容
        print("在 <h2> requires </h2> 和 <h2> provides </h2> 之间的 <p> 标签内容：")
        require = []
        for p in paragraphs:
            print(p.text)
            p = str(p.text)
            req_name, req_version = p.split(' ', 1)
            print(req_name, req_version)
            # dependent package informaiton
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
        "PkgName": package_name,
        "package_size": content_length,
        "OriginalVersion":OriginalVersion,
        "FixedVersion":FixedVersion,
        "website": website,
        "path": path_text,
        "requires": require,
    }

    return data



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


if __name__ == "__main__":
    print(get_package_information('npm 6.14.6','1.4.28','6.14.6'))
