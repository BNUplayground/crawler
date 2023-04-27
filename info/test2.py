import csv
import json

# 打开JSON文件
with open('share_file\crawler\info\history.json', 'r', encoding='utf-8') as f:
    data = f.readlines()

# 写入CSV文件
with open('share_file\crawler\info\\testoutput2.csv', 'w', newline='') as f:
    writer = csv.writer(f)

    # 写入表头
    writer.writerow(["Size"])

    # 写入数据行
    for item in data:
        item = json.loads(item)
        size = item["Size"]
        if size.endswith("MB") and size != "0MB":
            size_in_b = int(float(size[:-2]) * 1024 * 1024)
            writer.writerow([size_in_b])
