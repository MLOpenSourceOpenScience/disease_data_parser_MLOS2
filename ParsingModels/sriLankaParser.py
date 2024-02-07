"""
Sri Lanka Parser

Author: MLOS^2_NLP_TEAM
Date: 2024.02.06
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../ParsingModels')) # Gets the directory of SriLankaModules for importing dependencies
sys.path.append(os.path.join(os.path.dirname(__file__), '../Modules')) # Gets the directory of LLaMaInterface module for import
# Gets the directory of SriLankaModules for importing dependencies

from typing import List
from SriLankaModules.convert_to_table import convert_to_table, tableHeading, print_table
from SriLankaModules.rtfExtractor import extractDataFromRTF

def extractToTable(rtfData: str, flags: List[str] = []) -> [List[List[str]], List[str]]:
    debug_mode = '-d' in flags
    if debug_mode:
        print("DEBUG - Raw Text Data:")
        print(rtfData)
    important_text,timestamps = extractDataFromRTF(rtfData)
    if debug_mode:
        print("DEBUG - Extracted Text and Timestamp:")
        print(important_text)
        print(timestamps)
    table = convert_to_table(important_text,timestamps)
    heading = tableHeading #tableHeading imported from SriLankaModules.convert_to_table

    if debug_mode:
        print("DEBUG - Output Table:")
        print_table(table)

    return table, heading

if __name__ == '__main__':
    print("testing")
