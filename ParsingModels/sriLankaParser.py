"""
Sri Lanka Parser

Author: MLOS^2_NLP_TEAM
Date: 2024.02.06
"""

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
