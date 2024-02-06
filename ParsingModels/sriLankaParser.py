import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../ParsingModels')) # Gets the directory of SriLankaModules for importing dependencies
sys.path.append(os.path.join(os.path.dirname(__file__), '../Modules')) # Gets the directory of LLaMaInterface module for import
"""
Sri Lanka Parser

Author: MLOS^2_NLP_TEAM
Date: 2024.02.06
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../ParsingModels'))
# Gets the directory of SriLankaModules for importing dependencies

from typing import List
from SriLankaModules.convert_to_table import convert_to_table, tableHeading
from SriLankaModules.rtfExtractor import extractDataFromRTF

def extractToTable(rtfData: str) -> [List[List[str]], List[str]]:
    important_text,timestamps = extractDataFromRTF(rtfData)
    table = convert_to_table(important_text,timestamps)
    heading = tableHeading #tableHeading imported from SriLankaModules.convert_to_table
    return table, heading

if __name__ == '__main__':
    print("testing")
