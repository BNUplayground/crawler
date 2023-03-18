import requests
import json
image_name = 'library/python'
tag = '3.9.16-bullseye'
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

    registry_api_url = "https://registry.hub.docker.com/v2/{0}/manifests/{1}".format(
        image_name, tag)

    response = requests.get(registry_api_url, headers=headers)
    response_data = json.loads(response.text)

    print(response_data)

    layers = response_data["layers"]

# 遍历每个层，获取层的哈希值和大小
for layer in layers:
    layer_digest = layer["digest"]
    layer_size = layer["size"]
    print("Layer digest: {0}".format(layer_digest))
    print("Layer size: {0}".format(layer_size))
