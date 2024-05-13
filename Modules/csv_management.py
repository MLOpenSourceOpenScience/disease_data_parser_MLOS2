'''
Extract target data from csv file / order, and manage file data

This model will be responsible for extracting the data for user's need,
such as data of a single diseases, or single location.

Author: MLOS^2_NLP_TEAM
Date: 2024.02.06
'''

import os
import csv
import re
from typing import Tuple


def source_control(input_file: str, output_file: str) -> Tuple[str, str]:
    '''
    Reads two strgin, and creats path if it is unavailable yet.

    Then, return two paths.

    Parameters:
    - input_file (str): Location of an input file.
    - ouput_file (str): Location of an output file.

    Returns:
    - str: path of an input file.
    - str: path of an output file.
    '''

    file_path = os.path.join(
        os.path.dirname(os.path.join(os.path.dirname(__file__), '../')),
        input_file
    )

    if not os.path.exists(file_path):
        print(f"ERROR: File '{file_path}' does not exists.")
        raise FileNotFoundError

    output_path = os.path.join(
        os.path.dirname(os.path.join(os.path.dirname(__file__), '../')),
        output_file
    )

    output_directory = os.path.dirname(output_path)

    if not os.path.exists(output_directory):
        # if there's no outputfile already, create one.
        os.makedirs(output_directory)

    return file_path, output_path


def extract_data(target: str, filename: str = 'Out/output.csv', outfile: str = None) -> None:
    '''
    Extract data using given target.

    This fuction will determine whether the given target is location or
    diseases, or even something else.

    Parameters:
    - filename (str): Location of a csv file.
    - target (str): target that user wants to find.
    - outfile (str): location of an output file, default as 'Out/output+
                     (target string).csv'
    '''

    default_location = filename.split('.')[0]
    default_location = default_location + '_' + target + '.csv'

    if outfile is None:
        outfile = default_location

    file_path, output_path = source_control(filename, outfile)

    column = None
    new_file_data = []

    target = target.lower()

    first_row = None

    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)

        for row in reader:
            if first_row is None:
                first_row = row
            elif column is not None and row and target == row[column]:
                new_file_data.append(row)
            elif row:
                for i, element in enumerate(row):
                    if element.lower() == target:
                        column = i
                        new_file_data.append(row)

    with open(output_path, 'w', newline='', encoding='utf-8') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(first_row)
        writer.writerows(new_file_data)


def time_numeric_conversion(given: str, direction: bool = True) -> str:
    '''
    convert time -> nemeric time or vice versa,
    prior to sorting the data.
    '''

    month_mapping = {
        'Jan': '01',
        'Feb': '02',
        'Mar': '03',
        'Apr': '04',
        'May': '05',
        'Jun': '06',
        'Jul': '07',
        'Aug': '08',
        'Sep': '09',
        'Oct': '10',
        'Nov': '11',
        'Dec': '12'
    }

    if direction:
        pattern = r'(\d{2})-(\w{3,8})-(\d{4})'

        match = re.search(pattern, given)

        if match:
            day = match.group(1)
            month = match.group(2)
            year = match.group(3)

            month = month_mapping.get(month, month)

            return_string = year+month+day
            return return_string

    month_mapping_reverse = {v: k for k, v in month_mapping.items()}
    month = month_mapping_reverse.get(given[4:6], given[4:6])

    return_string = given[6:]+'-'+month+'-'+given[:4] + ' 00:00:00'
    return return_string


def order_by_time(filename: str = 'Out/output.csv', outfile: str = None, asc: bool = True) -> None:
    '''
    order the csv file by timestamp
    '''

    if outfile is None:
        outfile = filename

    file_path, output_path = source_control(filename, outfile)

    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row['TimeStampStart'] = time_numeric_conversion(
                row['TimeStampStart'])
            data.append(row)

    sorted_data = sorted(
        data, key=lambda x: x['TimeStampStart'], reverse=False if asc else True)

    with open(output_path, 'w', newline='', encoding='utf-8') as file:
        fieldnames = sorted_data[0].keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for row in sorted_data:
            row['TimeStampStart'] = time_numeric_conversion(
                row['TimeStampStart'], False)
            writer.writerow(row)


if __name__ == '__main__':
    T = ['Dengue Fever', 'Dysentery', 'Encephalitis', 'Enteric Fever', 'Food Poisoning', 'Leptospirosis',
         'Typhus Fever', 'Viral Hepatitis', 'Human Rabies', 'Chickenpox', 'Meningitis', 'Leishmaniasis']

    for t in T:
        extract_data(t)
    # extract_data("Colombo", 'Out/output_dengue fever.csv')
    # extract_data("Gampaha", 'Out/output_dengue fever.csv')
    # extract_data("Kalutara", 'Out/output_dengue fever.csv')
    # extract_data("Kandy", 'Out/output_dengue fever.csv')
    # extract_data("Matale", 'Out/output_dengue fever.csv')
    # extract_data("NuwaraEliya", 'Out/output_dengue fever.csv')
    # extract_data("SRILANKA", 'Out/output_dengue fever.csv')

    # order_by_time("Out/output_dengue fever.csv")
