import csv
import os
#读取data.csv文件
with open('./dependency/data.csv')as f:
    reader = csv.DictReader(f)
    for row in reader:
    #获取包名和下载ur1
        package_name = row['package_name']
        # download_url = row['download_url']
        # #下载deb包到当前目录
        # os.system('wget -o ./dependency/{0} {1}'.format(package_name,download_url))
        #读取deb包的依赖信息
        depends = os.popen('dpkg -I {0} | grep Depends'.format(package_name)).read().strip().replace('\n', ' ')
        #保存依赖信息到output.csv文件
        size = os.path.getsize("/path/to/file.mp3")
        print(package_name, size)
        with open('dependency/output.csv','a')as f:
            writer = csv.writer(f)
            writer.writerow([package_name, size, depends])