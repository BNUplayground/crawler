import json

with open('syft/temp.json', 'r') as f:
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
    print('--------------------------------------------------')