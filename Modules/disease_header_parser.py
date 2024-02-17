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

def compare_two_word(str1: str, str2: str) -> int:
    """"
    Input two string, then compute the similarity (Max as 1).

    Parameters:
    - str1 (str): First string. (name search from rtf)
    - str2 (str): Second string. (name from DB)

    Returns:
    - int: Score of similarity.
    """

    temp_score = 0.0

    str1 = str1.lower()
    str2 = str2.lower()
    # Not case sensitve!!
    # Python compare words with case sensitive measure.

    # First, need to check whether the string is two-length or one.
    str1_list = str1.split()
    is_two_word1 = False

    if len(str1_list) > 1:
        is_two_word1 = True

    str2_list = str2.split()
    is_two_word2 = False

    if len(str2_list) > 1:
        is_two_word2 = True

    if is_two_word1 and not is_two_word2:
        # the case where name is two length but db is one-word.
        ## So automatically 0.
        return 0

    if not is_two_word1 and not is_two_word2:
        lc = longest_common_subsequence(str1, str2)
        temp_score = lc / max(len(str1), len(str2))
        # normalize so that maximum is 1.
        ## (Portion of maximum subsequence from the maximum word)
    elif not is_two_word1 and is_two_word2:
        # since we don't hope the word to match second word, abort the second similarity
        lc1 = longest_common_subsequence(str1, str2_list[0])
        temp_score = lc1 / max(len(str1), len(str2_list[0]))
    elif is_two_word1 and is_two_word2:
        lc1 = longest_common_subsequence(str1_list[0], str2_list[0])
        lc2 = longest_common_subsequence(str1_list[1], str2_list[1])
        max_length1 = max(len(str1_list[0]), len(str2_list[0]))
        max_length2 = max(len(str1_list[1]), len(str2_list[1]))
        temp_score = ((lc1 / max_length1) + (lc2 / max_length2)) / 2

    return temp_score

def longest_common_subsequence(str1: str, str2: str, index1: int = None, index2: int = None) -> int:
    """
    Input two string, then compare to have longest substring.

    Parameters:
    - str1 (str): First string.
    - str2 (str): Second string.
    - index1 (int): Index of first string.
    - index2 (int): Index of second string.

    Returns:
    - int: maximum subsequence.
    """
    if index1 is None:
        index1 = len(str1) - 1
    if index2 is None:
        index2 = len(str2) - 1

    if index1 < 0 or index2 < 0:
        return 0

    if str1[index1] == str2[index2]:
        return 1 + longest_common_subsequence(str1, str2, index1-1, index2-1)

    return max(longest_common_subsequence(str1, str2, index1, index2-1),
                longest_common_subsequence(str1, str2, index1-1, index2))

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
                    # for now append error, but later make this to import new words into library
                    parsed_names.append(
                        f'Error detected with name: {name}. Please check the dictionary')

    return parsed_names

#example code
if __name__ == "__main__":

    PARSE_LINE = ("DPDHS\n Division  Dengue Fe-\n"+
                  "ver / DHF* Dysentery Encephali\n"+
                  "tis  Enteric\nFever Food\nPoisoning\n"+
                  "  Leptospiro\nsis Typhus\nFever Viral\nHepatitis")
    # print(detect_diseases(PARSE_LINE))

    print(compare_two_word("Dengue", "D"))
    print(compare_two_word("Dengue", "Dengue fever"))
    print(compare_two_word("Dengue fever", "d fever"))
