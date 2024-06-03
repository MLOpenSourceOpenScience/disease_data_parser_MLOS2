
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
from table_conversion_functions import time_to_excel_time, remove_blank_values, print_table

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


def is_number_value(input_string: str) -> bool:
    """
    Check if the input strging can tranlated into number

    Parameters:
    - input_string (str): String evaluated.

    Returns:
    - bool: True if it is, False if it is not.
    """
    if input_string[-1] in ['%']:
        input_string = input_string[:-1]
    elif '+' in input_string:
        index_int = input_string.find('+')
        input_string = input_string[:index_int]
    elif input_string == 'v':
        input_string = '0'

    try:
        float(input_string) #If it can cast to float, it is a number
    except ValueError:
        # if alphabetic or special characetr
        return False
    return True


# Assumes `text` only contains the table.
## if it contains more (especially at the beginning), it will give erroneous results
# first_location should only have table values after it
def get_table_values(first_location: str, text: str, flags: List[str] = None) -> Optional[str]:
    """
    Format values into table format then return as a 2D array. Return None if error.

    Parameters:
    - first_location (str): 
    - text (str): Huge line of string that has seperated with newline characters.
    - flag (List[str]): List of flags that will sent through main

    Returns:
    - Optional[str]: Parsed list of text that contains value as table.
    """
    start_index = text.find(first_location)
    debug_mode = flags is not None and '-d' in flags

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
                if len(row) > 1:
                    # Having number of 1 means there 'is' an error.
                    ## Or, it might having one number such as year, or number of reports,
                    ## or something inconsistant with the real data, so remove it.
                    output.append(row)
                row = []
        if len(row) > 1:
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

def header_concatenation(data: List[str]) -> List[str]:
    """
    Bring strings that are supposed to be a header and make those names
    into one line so that it could readed as a header from other funct-
    ions.

    Parameters:
    - data (List[str]): data

    Returns:
    - List(str): Modified list of strings where consecutive headers are
        concatenated.
    """

    i = 0
    while i < len(data) - 1:
        row = data[i]
        next_row = data[i + 1]

        row_state = row[0].isalpha() and (row[-1].isalpha() or
                                          row[-1] in ['-', '.'])
        next_row_state = next_row[0].isalpha() and (next_row[-1].isalpha() or
                                                    next_row[-1] in ['-', '.'])

        ab_row = (row[-1] == 'A' and next_row[0] == 'B') or (row[-1] == 'B' and next_row[0] == 'A')
        ad_tc = (row[-1] == 'B' and next_row == 'T*') or (row[-1] == '*' and next_row == 'C**')

        if row_state and next_row_state and next_row != 'A' and next_row[0:2] != 'Co':
            data[i] = row + ' ' + next_row
            del data[i + 1]
        elif ab_row or ad_tc:
            data[i] = row + ' ' + next_row
            del data[i + 1]
        else:
            i += 1

    return data



def convert_to_table(important_text: List[str],
                     timestamps: List[datetime],
                     flags: List[str] = None) -> List[str]:
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
    debug_mode = flags is not None and '-d' in flags

    table_data = []
    rows = important_text[1].split('\n')
    rows = remove_blank_values(rows)
    # Sometimes, important_tex will have '\n' in the header as well
    # Thus, there might need a function that works as concatination
    # of those strings
    rows = header_concatenation(rows)
    if(len(rows) == 0):
        print("\n\n\nNo rows found\n\n\n")
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

    # pre-process, such as removing 0, 5, 4 in front of location names

    #TODO: generalize the method to fix specific errors...maybe
    for i in range(2, len(rows)):
        temp = rows[i].strip()
        if temp == "M31atale":
            rows[i] = "Matale"
        elif temp in ["SRI LANKA", "SRI"]:
            rows[i] = "SRILANKA"
        elif is_number_value(temp[0]) and temp[1:].isalpha() and len(temp) > 4:
            rows[i] = temp[1:]

    new_rows = [rows[0]]
    temp_row = rows[1]

    for i in range(2, len(rows)):
        if ((rows[i].strip()[0].isalpha() or rows[i].strip()[-1].isalpha())
            and not rows[i].strip() == 'v' and not rows[i][-1] == 'Q'):
            new_rows.append(temp_row.strip())
            temp_row = rows[i]
        else:
            temp_row += " " + rows[i]

    new_rows.append(temp_row)
    rows = new_rows

    if debug_mode:
        print("DEBUG: LABELS:")
        print(labels)
        print("DEBUG: ROWS:")
        for row in rows:
            print("row: ",row)

    for i in range(2,len(rows)):
        data = rows[i].strip().split(" ") # Splits row into data
        data = remove_blank_values(data) # Removes empty entries in data (such as '')

        location_name = data[0]

        # RTF reader often can't detect where the table ends.
        # However since it mostly ends with "Source:", set the string
        # as a breakpoint and break if the first word of the row is that.

        stop_reading = False

        break_strings = ["Source:", "WRCD", "PRINTING", "Table", "Page"]
        for break_string in break_strings:
            if data[0][:len(break_string)] == break_string:
                stop_reading = True

        if stop_reading:
            break

        if table_values is None:
            table_values = get_table_values(location_name, important_text[1], flags)
            if debug_mode:
                print("DEBUG: TABLE VALUES:")
                for row in table_values:
                    print("Row Length:", len(row), row)

        long, lat, region_type, country_code, region_boundary = get_location_info(location_name)
        for j in range(1,len(data)-3,2):
            cases = table_values[i-2][j-1]
            #print("data:", data)
            #print("labels:", labels)
            #print("j:", j)
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
    print_table(table, tableHeading)
    from table_to_csv import print_to_csv
    print_to_csv(table,tableHeading)
