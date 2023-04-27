import csv
import json

# 打开JSON文件
with open('share_file\crawler\info\inspect.json', 'r') as f:
    data = json.load(f)

# 写入CSV文件
with open('share_file\crawler\info\\testoutput.csv', 'w', newline='') as f:
    writer = csv.writer(f)

    # 写入表头
    writer.writerow(["RepoTags", "Architecture", "Os", "Size",
                    "Layer_hash", "Layer_number", "Layer_size"])

    # 写入数据行
    for item in data:
        for layer_number, layer in enumerate(item["RootFS"]["Layers"]):
            writer.writerow([
                ",".join(item["RepoTags"]),
                item["Architecture"],
                item["Os"],
                item["Size"],
                layer,
                layer_number+1,
                len(layer)
            ])
