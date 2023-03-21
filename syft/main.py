import json
import csv
import os
filename='data/image_stats.csv'
images = []

with open(filename, 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        images.append(row[0])

print(images)

f = open('syft/res.csv', 'a+')

csv_writer = csv.writer(f)

for i in range(21, len(images)):
    image = images[i]
    data_row = [image]
    print(image)
    if image == "aerospike":
        image = image + ":ee-6.2.0.7_1"
    if image == "haskell":
        image = image + ":9.2.7-slim-buster"
    os.system(f'docker pull ' + image)
    os.system(f'syft '+ image + ' -o spdx-json=syft/data.json')
    with open('syft/data.json', 'r') as f:
        data = json.load(f)
    packages = data.get("Results")
    # Extract the required information
    name = data.get("name")
    print(name)
    packages = data.get("packages")
    # print(image)
    for package in packages:
        print('package:', package.get('name'))
        print('version:', package.get('versionInfo'))
        csv_writer.writerow(data_row + [package.get('name'), package.get('versionInfo')])
    # clear content inside
    print('--------------------------------------------------')

# res = data['Results']