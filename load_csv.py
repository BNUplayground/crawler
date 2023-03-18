import csv
filename='./image_stats.csv'

images = []

with open(filename, 'r') as file:
    csv_reader = csv.reader(file)
    header = next(csv_reader)
    for row in csv_reader:
        images.append(row[0])

print(images)