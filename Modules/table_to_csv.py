"""
Table to CSV

for now, it only supports one function:
writing a given data into csv.

Author: MLOS^2_NLP_TEAM
Date: 2024.02.05
"""

import os
import csv
from typing import List

def print_to_csv(table: List[List[str]],
                 headings: List[str] = None,
                 file_name: str = '../Out/output.csv') -> None:
    """
    Get the table data and headings, with the name of new output file.
    Then creates file with the name given, using header, creates csv
    file that holds the information given as a table format.

    Parameters:
    - table (List[List[str]]): The information stored as a 2D array.
    - headings (List[str]): Header for the information given.
    - file_name (str): Name of the ouput file (csv).
    
    Returns:
    - None
    """

    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), file_name)
    # dynamic name available by user's taste

    file_directory = os.path.dirname(file_path)
    # if file is not available ( not existing on the first place )

    if not os.path.exists(file_directory):
        # if there's no outputfile already, create one.
        os.makedirs(file_directory)

    with open(file_path, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        is_file_empty = os.path.getsize(file_path) == 0
        #Checks if file is empty, only empty files will get a heading

        if headings and is_file_empty:
            writer.writerow(headings)

    for row in table:
        with open(file_path, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(row)
