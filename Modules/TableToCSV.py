
import os
import csv
from typing import List

def printToCSV(table: List[List[str]], headings: List[str] = None, file_name: str = '../Out/output.csv') -> None:

    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), file_name)
    # dynamic name available by user's taste

    file_directory = os.path.dirname(file_path)
    # if file is not available ( not existing on the first place )

    if not os.path.exists(file_directory):
        # if there's no outputfile already, create one.
        os.makedirs(file_directory)

    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        is_file_empty = os.path.getsize(file_path) == 0
        #Checks if file is empty, only empty files will get a heading

        if headings and is_file_empty:
            writer.writerow(headings)

    for row in table:
        with open(file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row)