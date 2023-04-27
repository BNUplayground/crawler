import json
import csv
import os
filename='../data/new_image_list.csv'
images = []

with open(filename, 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        images.append(row[0])

print(images)

f = open('new_res2.csv', 'a+')

csv_writer = csv.writer(f)

for i in range(0, len(images)):
    image = images[i]
    data_row = [image]
    print(image)
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
    #os.system(f'docker pull ' + image)
    os.system(f'syft '+ image + ' -o json=syft/data2.json')
    with open('syft/data2.json', 'r') as f:
        data = json.load(f)
    packages = data.get("artifacts")
    # Extract the required information
    #name = data.get("name")
    #print(name)
    #packages = data.get("packages")
    # print(image)
    if packages:
        for package in packages:
            print('package:', package.get('name'))
            print('version:', package.get('version'))
            print('type:', package.get('type'))
            csv_writer.writerow(data_row + [package.get('name'), package.get('version'), package.get('type')])
        # clear content inside
        print('--------------------------------------------------')
    else:
        csv_writer.writerow(data_row)

# res = data['Results']
