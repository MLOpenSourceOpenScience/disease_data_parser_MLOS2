import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../ParsingModels')) # Gets the directory of SriLankaModules for importing dependencies
sys.path.append(os.path.join(os.path.dirname(__file__), '../Modules')) # Gets the directory of LLaMaInterface module for import

print(os.path.dirname(__file__))

from SriLankaModules.convertToTable import convertToTable, tableHeading
from SriLankaModules.rtfExtractor import extractDataFromRTF
from typing import *


def extractToTable(rtfData: str) -> [List[List[str]], List[str]]:
    importantText,timestamps = extractDataFromRTF(rtfData)
    table = convertToTable(importantText,timestamps)
    heading = tableHeading #tableHeading imported from SriLankaModules.convertToTable
    return table, heading

if __name__ == '__main__':
    print("testing")