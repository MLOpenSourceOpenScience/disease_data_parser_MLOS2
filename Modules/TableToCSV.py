import os
import csv
from typing import *

def printToCSV(table: List[List[str]], headings: List[str] = None, fileName: str = '../Out/output.csv') -> None:

    filePath = os.path.join(os.path.dirname(os.path.realpath(__file__)), fileName)
    # dynamic name available by user's taste

    fileDirectory = os.path.dirname(filePath)
    # if file is not available ( not existing on the first place )

    if not os.path.exists(fileDirectory):
        # if there's no outputfile already, create one.
        os.makedirs(fileDirectory)

    with open(filePath, 'a', newline='') as file:
        writer = csv.writer(file)
        isFileEmpty = os.path.getsize(filePath) == 0 #Checks if file is empty, only empty files will get a heading
        if headings and isFileEmpty:
            writer.writerow(headings)

    for row in table:
        with open(filePath, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row)