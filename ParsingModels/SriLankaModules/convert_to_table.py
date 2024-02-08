#Mahi
"""
Sri Lanka Convert to Table

Parsing model that is compatable with Sri Lanka data.
It will read the full text and parse it, making the
data readable using different modules in 'Modules'
folder.

Author: MLOS^2_NLP_TEAM
Date: 2024.02.06
"""

import sys
import os
from datetime import datetime,timedelta
from typing import List, Optional
import re

current_directory = os.path.dirname(__file__)
moudlues_directory = os.path.join(current_directory, '../../Modules')
sys.path.append(moudlues_directory)
# Gets the directory of Modules for import

from location_interface import get_location_info
from disease_header_parser import detect_diseases

# sys.path.append(os.path.join(os.path.dirname(__file__), '../LLaMa'))
# Gets the directory of LLaMaInterface module for import
# from LLaMaInterface import separateCellHeaders

tableHeading = ['Disease Name',
                'Cases',
                'Location Name',
                'Country Code',
                'Region Type',
                'Lattitude',
                'Longitude',
                'Region Boundary',
                'TimeStampStart',
                'TimeStampEnd']

def time_to_excel_time(time: datetime) -> str:
    """
    Get time as datetime format, and return str type of that same datetime.

    Parameters:
    - time (datetime): The time given.

    Returns:
    - str: The same time writen as a string.
    """
    return time.strftime("%d-%b-%Y %H:%M:%S")


# Table format: [Disease Name][Cases][Location Name][Country Code][Region Type(City/County/Country)]
#               [Lattitude][Longitude][Region Boundary][TimeStampStart][TimeStampEnd]

def is_number_value(input_string: str) -> bool:
    """
    Check if the input strging can tranlated into number

    Parameters:
    - input_string (str): String evaluated.

    Returns:
    - bool: True if it is, False if it is not.
    """
    try:
        float(input_string) #If it can cast to float, it is a number
    except ValueError:
        # if alphabetic or special characetr
        return False
    return True


# Assumes `text` only contains the table.
## if it contains more (especially at the beginning), it will give erroneous results
# first_location should only have table values after it
def get_table_values(first_location: str, text: str, flags: List[str] = []) -> Optional[str]:
    start_index = text.find(first_location)
    debug_mode = '-d' in flags

    if start_index != -1:
        parsed = text[start_index:]
        parsed = re.split('\n| ', parsed)
        parsed = remove_blank_values(parsed) # Removes empty entries in data (such as '')
        output = []
        row = []
        for data in parsed:
            if is_number_value(data):
                row.append(data)
            else:
                if len(row)>0:
                    output.append(row)
                row = []
        if len(row)>0:
            output.append(row)

        # Error checking len of each row
        row_lens = [len(row) for row in output]
        if len(set(row_lens)) != 1:
            print("WARNING: inconsistent rows in convert_to_table.get_table_values():")
            print(row_lens)
            if not debug_mode:
                print("run with -d (debug mode) to see more information")

        return output
    else:
        return None

# Removes blank values from a List
def remove_blank_values(data: List[str])-> List[str]:
    return list(filter(str.strip, data)) # Removes empty entries in data (such as '')


def convert_to_table(important_text: List[str],
                     timestamps: List[datetime],
                     flags: List[str] = []) -> List[str]:
    """
    Read text file and parse it, creating a List of string which holds
    the same information as a table format (2D). Will get a timestaps
    as a list of datetime seperately.

    Parameters:
    - important_text (str): Chunk of text file that will be parsed.
    - timestapes (List[datetime]): Two timestamp value (start, end)

    Returns:
    - List[str]: Parsed text in a table format.
    """
    table_values = None
    debug_mode = '-d' in flags

    table_data = []
    rows = important_text[0].split('\n')
    rows = remove_blank_values(rows)
    labels = detect_diseases(rows[0])
    # if __name__ == '__main__': #for testing
    #     labels = ['RDHS',
    #               'Dengue Fever',
    #               'Dysentery',
    #               'Encephalitis',
    #               'Enteric Fever',
    #               'Food Poisoning',
    #               'Leptospirosis',
    #               'Typhus',
    #               'Viral Hepatitis',
    #               'Human Rabies',
    #               'Chickenpox',
    #               'Meningitis',
    #               'Leishmaniasis',
    #               'WRCD']

    if debug_mode:
        print("DEBUG: ROWS:")
        print(rows)

    for i in range(2,len(rows)):
        data = rows[i].strip().split(" ") # Splits row into data
        data = remove_blank_values(data) # Removes empty entries in data (such as '')
        location_name = data[0]
        if table_values is None:
            table_values = get_table_values(location_name, important_text[1], flags)
            if debug_mode:
                print("DEBUG: TABLE VALUES:")
                for row in table_values:
                    print("Row Length:", len(row), row)

        long, lat, region_type, country_code, region_boundary = get_location_info(location_name)
        for j in range(1,len(data)-3,2):
            cases = table_values[i-2][j-1]
            disease_name = labels[j//2]
            # j//2 is to skip every other value,
            # since for Sri Lanka the tables have A and B values,
            # B values being cummulative(not useful for us)
            table_data.append([disease_name,
                          cases,
                          location_name,
                          country_code,
                          region_type,
                          lat,
                          long,
                          region_boundary,
                          time_to_excel_time(timestamps[0]),
                          time_to_excel_time(timestamps[1])])
    return table_data

def print_table(tabled_text: List[str])-> None:
    """
    Read table and print it as formatted output

    Parameters:
    - tabled_text (List[str]): data formatted as table
    """
    for heading in ['Disease Name',
                    'Cases',
                    'Location Name',
                    'Country Code',
                    'Region Type',
                    'Lattitude',
                    'Longitude',
                    'Region Boundary',
                    'TimeStampStart',
                    'TimeStampEnd']:
        print(f"|{heading:<15}",end=" ")
    print("|")
    for row in tabled_text:
        for col in row:
            print(f"|{col:<15}",end=" ")
        print("|")


if __name__ == '__main__':
    TEST_DATA = '''RDHS Dengue Fever Dysentery Encephaliti Enteric Fever Food Poi-
    Leptospirosis Typhus Viral Hep- Human Chickenpox Meningitis Leishmania- WRCD
A B A B A B A B A B A B A B A B A B A B A B A B T* C** 
Colombo 412 7733 0 5 0 9 0 1 0 6 7 156 0 0 0 3 0 0 3 151 3 22 0 5 23 100
Gampaha 351 7564 0 7 0 11 0 1 0 2 5 289 0 6 0 9 0 0 3 138 1 36 1 25 1 96 
Kalutara 192 2605 0 14 0 1 0 0 0 5 28 412 0 1 0 2 0 1 6 233 0 40 0 1 8 100 
Kandy 263 2594 0 18 0 0 0 4 0 12 8 132 2 36 0 2 0 1 2 137 0 11 1 15 83 100
Matale 43 723 0 2 0 0 0 1 0 5 4 86 0 9 0 3 0 0 3 30 0 3 5 159 19 100
NuwaraEliya 7 111 4 72 0 1 1 2 0 38 3 53 7 35 1 4 0 0 2 59 0 8 0 0 56 100
Galle 69 1161 3 25 0 11 0 5 0 18 14 492 0 26 0 1 0 1 7 180 0 11 0 1 32 100
Hambantota 82 813 0 4 2 3 0 1 0 8 14 174 2 46 0 7 0 0 1 85 0 14 22 308 22 100
Matara 48 876 2 19 1 6 0 0 2 9 20 317 0 18 0 2 0 1 5 141 1 10 7 87 49 100
Jaffna 51 1527 1 44 0 1 0 8 0 16 0 8 6 463 0 1 0 1 1 110 0 5 0 2 61 93 
Kilinochchi 2 64 0 4 0 0 0 0 0 16 0 7 1 6 0 0 0 0 0 8 0 0 0 0 17 98 
Mannar 4 66 0 6 0 0 0 1 0 0 3 27 0 5 0 0 0 0 0 1 1 4 0 0 26 100
Vavuniya 5 107 0 5 0 1 0 0 0 0 0 25 1 7 0 1 0 0 2 13 0 3 1 6 3 100
Mullaitivu 4 70 0 8 0 0 0 3 0 11 0 26 0 4 0 0 0 0 0 10 0 0 2 5 19 99 
Batticaloa 74 1648 3 127 0 6 0 3 4 16 2 58 0 1 0 3 0 1 2 38 1 23 0 1 53 100
Ampara 0 43 0 1 0 1 0 0 0 0 0 12 0 0 0 1 0 0 0 17 0 7 0 2 15 44 
Trincomalee 77 1704 0 5 0 1 0 0 0 4 2 54 0 13 0 0 0 0 2 30 0 17 0 1 20 100
Kurunegala 123 1673 1 20 0 7 0 0 0 2 19 203 0 9 0 8 0 2 2 255 1 76 8 231 19 100
Puttalam 53 2482 0 7 0 1 0 1 0 0 4 28 0 7 0 1 0 0 1 68 4 32 0 14 15 100
Anuradhapur 48 412 0 3 0 0 0 1 0 2 10 193 1 24 0 2 0 0 5 134 2 25 7 270 20 99 
Polonnaruwa 13 378 0 10 0 5 0 0 0 6 5 115 0 5 0 10 0 0 3 44 0 13 8 227 33 99 
Badulla 17 586 2 17 0 3 0 0 0 26 13 162 0 26 1 58 0 0 9 93 1 21 1 14 64 100
Monaragala 24 320 0 14 1 4 0 0 0 0 21 373 1 28 1 16 0 0 1 40 0 39 5 92 23 100
Ratnapura 82 1127 3 23 0 10 1 2 3 12 39 606 0 16 0 12 0 1 8 101 3 97 5 98 33 100
Kegalle 91 1557 1 12 0 1 0 2 0 8 22 352 1 19 0 3 0 0 5 219 1 33 1 18 28 100
Kalmune 29 1448 3 34 0 7 0 0 0 0 2 30 0 0 0 0 0 0 4 35 1 16 0 0 41 100
SRILANKA 216 39392 23 506 4 90 2 36 9 222 24 4390 22 810 3 149 0 9 77 2370 20 566 74 1582 33 98 '''

    table = convert_to_table(TEST_DATA,
                           [datetime(2023, 6, 9) +timedelta(days=-7),
                            datetime(2023, 6, 9)])
    print_table(table)
    from table_to_csv import print_to_csv
    print_to_csv(table,tableHeading)
