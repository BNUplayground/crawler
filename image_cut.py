import json
import csv
import os



filename='data/image_stats.csv'
images = []

with open(filename, 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        images.append(row[0])

def get_packages_and_sizes(image_name):
    try:
    	if image_name == 'fission/binary-env' or image_name == 'fission/go-env':
    	    return None
    	    
    	else:    
            output = os.popen(f"docker run --rm {image_name} dpkg-query -W --showformat='${{Installed-Size}} ${{Package}}\\n'").read()
    except Exception as e:
        print(f"镜像 {image_name} 查询失败: {e}")
        return None

    lines = output.strip().split("\n")
    packages_and_sizes = {}
    for line in lines:
        if not line:
            continue
        parts = line.split(" ", 1)
        if len(parts) != 2:
            print(f"跳过无法解析的行: {line}")
            continue
        try:
            size, package = parts
            packages_and_sizes[package] = float(size)
        except: 
            continue

    return packages_and_sizes

results = {}
for i in range(0, len(images)):
    image = images[i]
    data_row = [image]
    #print(image)
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

# for image_name in image_names:
    print(f"正在处理镜像 {image}")
    packages_and_sizes = get_packages_and_sizes(image)

    if packages_and_sizes is not None:
        results[image] = packages_and_sizes
        #print('seccess', image_name)

# 将结果保存到JSON文件
with open("results.json", "w") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("处理完成，结果已保存到results.json")
