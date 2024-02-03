import os
import csv
from typing import *

def printToCsv(table: List[List[str]], headings: List[str] = None, filePath: str = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../Out/output.csv')) -> None:

    with open(filePath, 'w', newline='') as file:
        writer = csv.writer(file)
        if headings:
            writer.writerow(headings)

    for row in table:
        with open(filePath, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row)