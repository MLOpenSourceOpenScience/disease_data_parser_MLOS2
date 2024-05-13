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
from datetime import datetime
from typing import List, Optional

current_directory = os.path.dirname(__file__)
moudlues_directory = os.path.join(current_directory, '../../Modules')
sys.path.append(moudlues_directory)
# Gets the directory of Modules for import

from location_interface import get_location_info
from disease_header_parser import detect_diseases
from table_conversion_functions import time_to_excel_time, remove_blank_values

# if header is needed, deal it here and reference it from parser. Otherwise,
# also can created header in the parser as well.

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
        output = []
        row = []
        row.append(text[start_index])


        # Assuming the row contains data as a form of 'location | data1 | data2 | data3...'
        for i in range(start_index, len(text)):
            if text[i].isnumeric():
                row.append(text[i])
            else:
                output.append(row)
                row = []
                row.append(text[i])

        return output

    return None

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
    # currently important text holds two values, using different rtf_reader (pdf -> rtf)
    ## Thus, if anything changes, change this function correspondingly.
    ## important text only means that it will hold reasonable, or required chunk of data.

    if len(rows) == 0:
        print("\n\n\nNo rows found\n\n\n")

    labels = detect_diseases(rows[0])
    # detect diseases will read single line then output the name of diseases that line holds.
    # if any new disease is added to given data, please modify "DiseaseDict.csv".

    new_rows = [rows[0]]
    temp_row = rows[1]
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
        # break_strings hold values which corresponds to Sri-Lanka data.
        ## updated it when needed

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
        # location info will return longitute, latitute, type of the region,
        # country code, then boundary using long/lat.
        ### Many location is added in 'LongLatDict.csv'.
        ### However in case of new location, it will automatically added, but if now, please check
        ### API key in Modules/location_interface.py in case of too many requests.

        for j in range(1, len(data)):
            cases = table_values[i][j]
            disease_name = labels[j]
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
