import json

# Load the JSON file
with open('./temp.json', 'r') as f:
    data = json.load(f)


metaData = data.get('Metadata')
# print(metaData.get('OS'))
# for meta in metaData:
#     print(meta)
print('RepoTags:', metaData.get('RepoTags'))
print('RepoDigests:', metaData.get('RepoDigests'))


# Extract the required information
image = data.get("Results")
# print(image)
for result in image:
    print('Target:', result.get('Target'))
    # print('RepoTags:', result.get['RepoTags'])
    # print('RepoDigests:', result.get['RepoDigests'])
    for vulnerability in result['Vulnerabilities']:
        print('VulnerabilityID:', vulnerability['VulnerabilityID'])
        print('InstalledVersion:', vulnerability['InstalledVersion'])
        print('FixedVersion:', vulnerability['FixedVersion'])
    print('--------------------------------------------------')
