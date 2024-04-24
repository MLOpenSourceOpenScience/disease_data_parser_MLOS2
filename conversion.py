import csv
import os
import sys
from collections import defaultdict

def split_file(in_csv_path:str, out_csv_path=None):
    disease = defaultdict(list)

    with open(in_csv_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)

        for row in reader:
            disease[row[0]].append(row)

    for disease_name, rows in disease.items():
        if out_csv_path is None:
            in_csv_path = in_csv_path.replace('\\', '/')

            path_folders = '/'.join(in_csv_path.split('/')[:-1])
            path_file = in_csv_path.split('/')[-1][:-4]

            path = f"SeparatedData/{path_folders}/{path_file}/"

            if not os.path.exists(path):
                os.makedirs(path)

            output_path = f"{path}{disease_name}.csv"
        else:
            output_path = out_csv_path

        with open(output_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(rows) 


def split_all_data():
    if len(sys.argv) < 2:
        print(f'please include an argument of where the folder is located')
        return
    inFolder = sys.argv[1]
    filesToParse = []
    if os.path.exists(inFolder):
        print("Locating files...")
        for root, dirs, files in os.walk(inFolder):
            for name in files:
                if name[-4:] == '.csv': # Only parse csv files
                    filesToParse.append(f'{root}/{name}'.replace('\\', '/'))
    print(f'files to separate: {filesToParse[:5]}')

    for file in filesToParse:
        split_file(file)


split_all_data()
