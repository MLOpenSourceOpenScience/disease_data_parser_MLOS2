"""
Template for the Parser

Author: MLOS^2_NLP_TEAM
Date: 2024.05.01
"""

import os
import sys

current_directory = os.path.dirname(__file__)
moudlues_directory = os.path.join(current_directory, '../Modules')
sys.path.append(moudlues_directory)

# Path of module files are added to system path.
# Required for usage of modules

from typing import List, Tuple
from ParsingModels.<Target Module>.<Target Extracter> import <extracter function name>
# Refer rtf_extractor at SriLankaModules. It should give the important text (what is relevant) then timestamp.
from ParsingModels.<Target Module>.<parsing module python file> import convert_to_table, tableHeading
# Refer brazil, then srilanka. These are two common structure of convert_to_table.
from table_conversion_functions import print_table

# Extra import files, import on demand

def extract_to_table(rtf_data: List[str],
                     flags: List[str] = None) -> Tuple[List[List[str]], List[str]]:
    """
    Get rtf data with flag and translate into 2D array (table)
    with Header.

    Supports various option if flag is on.

    Prarmeters:
    - rtf_data (List[str]): Data in rtf format.
    - flags (List[str]): Flag for options, such as debugging.

    Returns:
    - [List[List[str]], List[str]]: Table data, Header.
    """
    if flags is None:
        debug_mode = False
    else:
        debug_mode = '-d' in flags
    if debug_mode:
        print("DEBUG - Raw Text Data:")
        print(rtf_data)

    # -----Required if your data is in pdf, non-structured(raw-table from pdf or sliced unevenly after conversion) format-----
    # -----If this is not your case, your data is in bunch of csv or excel, continue to [P]-----

    if "-manual" in flags:
        important_text,timestamps = extract_data_from_rtf(rtf_data, True)
    else:
        important_text,timestamps = extract_data_from_rtf(rtf_data, False)

    # Important text will hold relevant value= the required data.
    ## Also, timestamp will be extracted as well

    if important_text is None or timestamps is None:
        print("Error: Timestamp recongnization error")
        return None, None
    
    # -----[P]-----

    # Data is organized, or was organized, so should convert it into table form

    if debug_mode:
        print("DEBUG - Extracted Text and Timestamp:")
        print(important_text)
        print(timestamps)

    table = convert_to_table(important_text, timestamps, flags = flags)
    # Convert to table will input all the data and then will re-structure it evenly
    # after the conversion, It should have a form of 2D array,

    ### [
    ###   [P1-name , data1 , data2 , data3],
    ###   [P2-name , dataA , dataB , dataC] 
    ### ]

    # or somewhat similar.
    # you can see the exact format as an output using print_table() function.

    heading = tableHeading

    # header of your desire.

    if debug_mode:
        print("DEBUG - Output Table:")
        print_table(table, heading)

    return table, heading


