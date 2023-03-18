import requests
import json
import csv
filename='./image_stats.csv'

f = open('test.csv', 'a+')

csv_writer = csv.writer(f)

images = []
data = [
    ["镜像名","下载量","tag","镜像大小", "层数量", "layer_number", "每个层哈希值", "每个层大小"]
]

with open(filename, 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        images.append(row[0])

print(images)

for i in range(147, 148):
    data_row = []
    image = images[i]
    if '/' in image:
        image_name = image
    else: 
        image_name = "library/" + image
    data_row.append(image)
    print("image_name", image)
    # 该docker所有的信息
    registry_api_url = "https://hub.docker.com/v2/repositories/{0}/".format(image_name)
    response = requests.get(registry_api_url)
    response_data = json.loads(response.text)

    # 下载量
    pull_count = response_data["pull_count"]
    data_row.append(pull_count)
    print("pull_count", pull_count)
    # tag信息
    registry_api_url = "https://hub.docker.com/v2/repositories/{0}/tags/".format(image_name)
    response = requests.get(registry_api_url)
    response_data = json.loads(response.text)

    # 最新tag
    tags = [tag["name"] for tag in response_data["results"]]
    tags_num = 0
    if tags[0] == 'latest' and len(tags) > 1:
        tags_num = 1
    data_row.append(tags[tags_num])
    print("tag-name", tags[tags_num])
    latest_tag = tags[0]
    # 最新tag的下载量
    tag_api_url = registry_api_url + latest_tag
    response = requests.get(tag_api_url)
    response_data = json.loads(response.text)

    # full size
    sizes = [tag["size"] for tag in response_data["images"]]
    image_size = sizes[0]
    data_row.append(image_size)
    print("image_size", image_size)

    tag = latest_tag
    headers = {'Accept': 'application/vnd.docker.distribution.manifest.v2+json'}

    # Get an access token from DockerHub
    auth_url = 'https://auth.docker.io/token'
    auth_params = {
        'service': 'registry.docker.io',
        'scope': f'repository:{image_name}:pull'
    }
    auth_response = requests.get(auth_url, params=auth_params)

    if auth_response.status_code == 200:
        auth_token = auth_response.json()['token']
        headers['Authorization'] = f'Bearer {auth_token}'

        registry_api_url = "https://registry.hub.docker.com/v2/{0}/manifests/{1}".format(image_name, tag)

        response = requests.get(registry_api_url, headers=headers)
        response_data = json.loads(response.text)
        if("layers" in response_data.keys()):
            layers = response_data["layers"]
            layers_len = len(layers)
        else:
            layers = None
            layers_len = 0

    # 遍历每个层，获取层的哈希值和大小
    data_row.append(layers_len)
    print("layers_number", layers_len)
    if layers_len == 0:
        csv_writer.writerow(data_row)
    for i in range(0, layers_len):
        layer_digest = layers[i]["digest"]
        layer_size = layers[i]["size"]
        csv_writer.writerow(data_row + [i, layer_digest, layer_size])
        print("Layer{0} digest: {1}".format(i,layer_digest))
        print("Layer{0} size: {1}".format(i,layer_size))

    # 镜像名 下载量 层数量 镜像大小 layer number 每个层哈希值 每个层大小


    