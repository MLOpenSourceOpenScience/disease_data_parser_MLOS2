import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../ParsingModels')) # Gets the directory of SriLankaModules for importing dependencies

from SriLankaModules.convertToTable import convertToTable
from SriLankaModules.rtfExtractor import extractDataFromRTF


def extractToTable(rtfData: str) -> list[list[str]]:
    importantText,timestamps = extractDataFromRTF(rtfData) #Eoin
    return convertToTable(importantText,timestamps) #Mahi

if __name__ == '__main__':
    print("testing")