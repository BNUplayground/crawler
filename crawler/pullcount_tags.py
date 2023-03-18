import requests
import json

image_name = "library/python"

# 该docker所有的信息
registry_api_url = "https://hub.docker.com/v2/repositories/{0}/".format(
    image_name)
response = requests.get(registry_api_url)
response_data = json.loads(response.text)

# 下载量
pull_count = response_data["pull_count"]
print(pull_count)
# tag信息
registry_api_url = "https://hub.docker.com/v2/repositories/{0}/tags/".format(
    image_name)
response = requests.get(registry_api_url)
response_data = json.loads(response.text)
print(response_data)

# 最新tag
tags = [tag["name"] for tag in response_data["results"]]
latest_tag = tags[0]
print(latest_tag)
# 最新tag的下载量
tag_api_url = registry_api_url + latest_tag
response = requests.get(tag_api_url)
response_data = json.loads(response.text)

sizes = [tag["size"] for tag in response_data["images"]]
first_size = sizes[0]
print(first_size)