"""
Disease Header Parser

Now supports parsing a given line into different
diseases by name.

Will support importing new disease into database
using user's input (user's favor).

Author: MLOS^2_NLP_TEAM
Date: 2024.02.05
"""

import os
import csv
from typing import List

def detect_diseases(line: str) -> List[str]:
    """
    Read line, and seperate the diseases by names.

    Parameters:
    - line (str): The list of names, seperated by space.

    Returns:
    - List[str]: names of diseases parsed
    """

    current_directory = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(current_directory, 'DiseaseDict.csv')

    names = line.lower().split()

    parsed_names = []

    double_length = False
    # flag for two-combined words

    for i in range(0, len(names)):
        if double_length:
            double_length = False
        else:
            with open(file_path, 'r', encoding= 'utf-8') as file:

                reader = csv.reader(file)
                name_found = False
                # for efficiency, if found, will break.

                for row in reader:

                    if name_found:
                        break
                    if i+1 < len(names) and row and row[0] == names[i]+' '+names[i+1]:
                        # check whether it is two-word combination before going through
                        parsed_names.append(row[1])
                        double_length = True
                        name_found = True
                    elif row and row[0] == names[i]:
                        if row[1] == "ignore":
                            # such as:
                            ## RDHS (location column), WRCD (time and percentage column),
                            ## or headers that does not have disease data in it.
                            pass
                        else:
                            parsed_names.append(row[1])
                        name_found = True

                if not name_found:
                    # for now append error, but later make this to import new words into library
                    parsed_names.append(f'Error detected with name: {names[i]}. Please check the dictionary')

    return parsed_names

#example code
if __name__ == "__main__":

    PARSE_LINE = "RDHS Dengue Fever Dysentery Encephaliti Enteric Fever Food Poi-Leptospirosis Typhus Viral Hep- Human Chickenpox Meningitis Leishmania- WRCD"

    print(detect_diseases(PARSE_LINE))
