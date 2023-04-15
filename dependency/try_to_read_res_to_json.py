import csv

import json
import chrome

def get_package_information(PkgName,OriginalVersion,FixedVersion):
    
    return_set = {}


def get_risk_information(VulnerabilityID,OriginalVersion,
                         FixedVersion,PkgName,Severity):
    # TODO finish the function 
    return_set = {}


def read_csv_write_json(csv_path, json_path):
    # Read the CSV file and extract the data
    with open(csv_path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        data = []
        for row in reader:
            image_name = row[0]
            VulnerabilityID = row[2]
            OriginalVersion = row[3]
            FixedVersion = row[4]
            PkgName = row[5]
            Severity = row[6]

            # TODO finish a function to get informaion in the 
            # form of Fixable_Risk from result json
            Fixable_Risk = []

            data.append({"image_name": image_name, "Fixable_Risk": Fixable_Risk})

    # Write the data to a JSON file
    with open(json_path, 'w') as jsonfile:
        json.dump(data, jsonfile)

if __name__ == "__main__":
    print(get_package_information('npm 6.14.6','1.4.28','6.14.6'))