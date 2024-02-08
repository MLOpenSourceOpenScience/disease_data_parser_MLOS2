"""
Sri Lanka Parser

Author: MLOS^2_NLP_TEAM
Date: 2024.02.06
"""
import sys
import os
from typing import List
sys.path.append(os.path.join(os.path.dirname(__file__), '../ParsingModels')) # Gets the directory of SriLankaModules for importing dependencies
sys.path.append(os.path.join(os.path.dirname(__file__), '../Modules')) # Gets the directory of LLaMaInterface module for import
# Gets the directory of SriLankaModules for importing dependencies

from SriLankaModules.convert_to_table import convert_to_table, tableHeading, print_table
from SriLankaModules.rtfExtractor import extract_data_from_rtf

def extract_to_table(rtf_data: List[str], flags: List[str] = None) -> [List[List[str]], List[str]]:
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
    important_text,timestamps = extract_data_from_rtf(rtf_data)

    if important_text is None or timestamps is None:
        print("Error: timestamp recongnization error")
        return None, None

    if debug_mode:
        print("DEBUG - Extracted Text and Timestamp:")
        print(important_text)
        print(timestamps)
    table = convert_to_table(important_text, timestamps, flags = flags)
    heading = tableHeading #tableHeading imported from SriLankaModules.convert_to_table

    if debug_mode:
        print("DEBUG - Output Table:")
        print_table(table)

    return table, heading

if __name__ == '__main__':
    print("testing")
