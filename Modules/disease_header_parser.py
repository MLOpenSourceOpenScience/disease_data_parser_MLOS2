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

    line = line.replace("\n","")
    line = line.replace("-","")
    # remove both newline character and '-'
    # also change double-space into single space

    names = line.lower().split()

    parsed_names = []

    double_length = False
    # flag for two-combined words

    for name, next_name in zip(names, names[1:]):
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
                    if next_name and row and row[0] == name+' '+next_name:
                        # check whether it is two-word combination before going through
                        parsed_names.append(row[1])
                        double_length = True
                        name_found = True
                    elif row and row[0] == name:
                        if row[1] == "ignore":
                            # such as:
                            ## RDHS (location column), WRCD (time and percentage column),
                            ## or headers that does not have disease data in it.
                            pass
                        else:
                            parsed_names.append(row[1])
                        name_found = True

                if not name_found:
                    print(f"Error: couldn't parse disease name: {name}. Please check the dictionary")
                    raise ValueError
                    # for now append error, but later make this to import new words into library
                    #parsed_names.append(
                        #f'Error detected with name: {name}. Please check the dictionary')

    return parsed_names

#example code
if __name__ == "__main__":

    PARSE_LINE = ("DPDHS\n Division  Dengue Fe-\n"+
                  "ver / DHF* Dysentery Encephali\n"+
                  "tis  Enteric\nFever Food\nPoisoning\n"+
                  "  Leptospiro\nsis Typhus\nFever Viral\nHepatitis")
    print(detect_diseases(PARSE_LINE))
