import json
import csv
import os
filename='data/upd_images.csv'
images = []

with open(filename, 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        images.append(row[0])

dic = {}
with open('./crawler/output.csv', 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        if row[0] not in dic:
            dic[row[0]] = row[1]

f = open('info/res.csv', 'a+')

csv_writer = csv.writer(f)

# 写入表头
csv_writer.writerow(["Image_name", "RepoTags","Download_counts", "Architecture", "Os", "Size",
                "Layer_hash", "Layer_number","Layer_allCount", "Layer_size"])

for i in range(0, len(images)):
    image = images[i].strip()
    data_row = []
    download_counts = dic[image.split(':')[0]]
    if image == "aerospike":
        image = image + ":ee-6.2.0.7_1"
    if image == "haskell":
        image = image + ":9.2.7-slim-buster"
    if image == "logstash":
        image = image + ":8.6.2"
    if image == "t4cc0re/php-env":
        image = image + ":7.1-cli"
    if image == "oraclelinux":
        image = image + ":7.9"
    if image == "java":
        image = image + ":6"
    if image == 'jenkins':
        image = image + ":2.60.3"
    if image == 'kibana':
        image = image + ":8.6.2"
    if image == 'elasticsearch':
        image = image + ":8.6.2"
    os.system(f'docker inspect ' + image + ' > info/inspect.json')
    with open('./info/inspect.json', 'r') as f:
        inspect_data = json.load(f)
    # 写入数据行
    image_size = 0
    for item in inspect_data:
        for layer_number, layer in enumerate(item["RootFS"]["Layers"]):
            data_row.append([image, "".join(item["RepoTags"]).split(":")[1], download_counts, item["Architecture"], item["Os"], item["Size"], layer, layer_number+1, len(item["RootFS"]["Layers"])])
            # csv_writer.writerow([
            #     ",".join(item["RepoTags"]),
            #     item["Architecture"],
            #     item["Os"],
            #     item["Size"],
            #     layer,
            #     layer_number+1,
            #     len(item["RootFS"]["Layers"])
            # ])
        image_size = item["Size"]

    command = "docker history --format '{{json .}}' " +  image + " > info/history.json"
    os.system(command)
    with open('./info/history.json', 'r', encoding='utf-8') as his:
        history_data = his.readlines()
    # 打开JSON文件
    contain_0b = False
    cnt = 0
    layer_size_sum = 0
    # 写入数据行
    if len(item["RootFS"]["Layers"]) == len(history_data):
       contain_0b = True
    # print(len(item["RootFS"]["Layers"]), len(history_data))
    image_data = []
    for item_num, item in enumerate(history_data):
        # print(len(data_row), item_num, cnt, contain_0b)
        item = json.loads(item)
        size = item["Size"]
        if size == "0B" and contain_0b:
            continue
        if size.endswith("G"):
            size_in_b = int(float(size[:-1]) * 1024 * 1024 * 1024)
            image_data.append(data_row[item_num if contain_0b else cnt] + [size_in_b])
            layer_size_sum += size_in_b
            cnt += 1
        elif size.endswith("GB"):
            size_in_b = int(float(size[:-2]) * 1024 * 1024 * 1024)
            image_data.append(data_row[item_num if contain_0b else cnt] + [size_in_b])
            layer_size_sum += size_in_b
            cnt += 1
        elif size.endswith("MB"):
            size_in_b = int(float(size[:-2]) * 1024 * 1024)
            image_data.append(data_row[item_num if contain_0b else cnt] + [size_in_b])
            layer_size_sum += size_in_b
            cnt += 1

        elif size.endswith("kB") :
            size_in_b = int(float(size[:-2]) * 1024)
            image_data.append(data_row[item_num if contain_0b else cnt] + [size_in_b])
            layer_size_sum += size_in_b
            cnt += 1

        elif size.endswith("B") and size != "0B":
            size_in_b = int(float(size[:-1]))
            image_data.append(data_row[item_num if contain_0b else cnt] + [size_in_b])
            layer_size_sum += size_in_b
            cnt += 1
    # print(image_size, layer_size_sum, (layer_size_sum - image_size) / image_size)
    for row in image_data:
        row[5] = layer_size_sum
        csv_writer.writerow(row)
# res = data['Results']