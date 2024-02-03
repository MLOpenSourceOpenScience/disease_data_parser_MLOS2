import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../ParsingModels')) # Gets the directory of SriLankaModules for importing dependencies

print(os.path.dirname(__file__))

from SriLankaModules.convertToTable import convertToTable, tableHeading
from SriLankaModules.rtfExtractor import extractDataFromRTF
from typing import *


def extractToTable(rtfData: str) -> List[List[str]]:
    importantText,timestamps = extractDataFromRTF(rtfData)
    return convertToTable(importantText,timestamps), tableHeading

if __name__ == '__main__':
    print("testing")