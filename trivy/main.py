import json
import csv
import os
filename='data/image_stats.csv'
images = []

with open(filename, 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        images.append(row[0])
        print(row[0])

print(images)

f = open('trivy/res.csv', 'a+')

csv_writer = csv.writer(f)

for i in range(15, len(images)):
    image = images[i]
    data_row = []
    print(image)
    os.system(f'docker pull ' + image)
    os.system(f'trivy image --ignore-unfixed '+ image + ' -f json -o trivy/temp.json')
    with open('trivy/temp.json', 'r') as f:
        data = json.load(f)
    metaData = data.get('Metadata')
    # print(metaData.get('OS'))
    # for meta in metaData:
    #     print(meta)
    print('RepoTags:', metaData.get('RepoTags'))
    data_row.append(metaData.get('RepoTags'))
    print('RepoDigests:', metaData.get('RepoDigests'))
    data_row.append(metaData.get('RepoDigests'))
    # Extract the required information
    image = data.get("Results")
    # print(image)
    for result in image:
        print('Target:', result.get('Target'))
        # print('RepoTags:', result.get['RepoTags'])
        # temp_data = data_row
        # print('RepoDigests:', result.get['RepoDigests'])
        if "Vulnerabilities" in result.keys():
            for vulnerability in result['Vulnerabilities']:
                # temp_data.append(vulnerability['VulnerabilityID'])
                print('VulnerabilityID:', vulnerability['VulnerabilityID'])
                # temp_data.append(vulnerability['InstalledVersion'])
                print('InstalledVersion:', vulnerability['InstalledVersion'])
                # temp_data.append(vulnerability['FixedVersion'])
                print('FixedVersion:', vulnerability['FixedVersion'])
                csv_writer.writerow(data_row + [vulnerability['VulnerabilityID'], vulnerability['InstalledVersion'], vulnerability['FixedVersion']])
        else:
            csv_writer.writerow(data_row)
        print('--------------------------------------------------')
# res = data['Results']