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
        temp_score = lc*2 / (len(str1) + len(str2))
        # normalize so that maximum is 1.
    elif not is_two_word1 and is_two_word2:
        # since we don't hope the word to match second word, abort the second similarity
        lc1 = longest_common_subsequence(str1, str2_list[0])
        if lc1 <= 1:
            temp_score = 0
        else:
            lc2 = longest_common_subsequence(str1, str2_list[1])
            length1 = (len(str1) + len(str2_list[0])) / 2
            length2 = (len(str1) + len(str2_list[1])) /2
            temp_score = ((lc1 / length1) + (lc2 / length2)) / 2
    elif is_two_word1 and is_two_word2:
        lc1 = longest_common_subsequence(str1_list[0], str2_list[0])
        lc2 = longest_common_subsequence(str1_list[1], str2_list[1])
        length1 = (len(str1_list[0]) + len(str2_list[0])) / 2
        length2 = (len(str1_list[1]) + len(str2_list[1])) / 2
        temp_score = ((lc1 / length1) + (lc2 / length2)) / 2

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
    line = line.replace(".","")
    line = line.replace("/","")
    # remove both newline character and '-', "."

    names = line.lower().split()
    names.append("eon")
    # end of name, for next_name parsing.

    parsed_names = []

    double_length = False
    # flag for two-combined words

    for name, next_name in zip(names, names[1:]):
        if double_length:
            double_length = False
        else:
            full_file = []

            with open(file_path, 'r', encoding= 'utf-8') as file:
                reader = csv.reader(file)
                full_file = list(reader)

            with open(file_path, 'r', encoding= 'utf-8') as file:

                reader = csv.reader(file)
                name_found = False
                # for efficiency, if found, will break.

                max_similarity = 0.0
                most_similar_word = ""
                target_word = ""

                for row in reader:
                    if not row:
                        break
                    if row[1] == "Real Name":
                        continue
                    name_list = row[0].split(",")

                    if name_found:
                        break
                    if next_name and name+' '+next_name in name_list:
                        # check whether it is two-word combination before going through
                        parsed_names.append(row[1])
                        double_length = True
                        name_found = True
                    elif name in name_list:
                        if row[1] == "ignore":
                            # such as:
                            ## RDHS (location column), WRCD (time and percentage column),
                            ## or headers that does not have disease data in it.
                            pass
                        else:
                            parsed_names.append(row[1])
                        name_found = True
                    else:
                        if row[1] == "ignore":
                            break
                        temp_score = compare_two_word(name, row[1])
                        if max_similarity < temp_score:
                            most_similar_word = name
                            max_similarity = temp_score
                            target_word = row[1]

                        if next_name:
                            temp_score = compare_two_word(name+' '+next_name, row[1])
                            if max_similarity < temp_score:
                                most_similar_word = name+' '+next_name
                                max_similarity = temp_score
                                target_word = row[1]

                if not name_found:
                    if max_similarity >= 0.5:
                        parsed_names.append(target_word)
                        if len(most_similar_word.split()) == 2:
                            double_length = True

                        for row in full_file:
                            if row and row[1] == target_word:
                                row[0] += ","+most_similar_word
                                break
                    else:
                        print(f"word '{name}' not found!")
                        print(f"Maximum similarity detected '{max_similarity}' for '{target_word}'.")
                        raise ValueError

            with open(file_path, 'w', newline='', encoding= 'utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(full_file)

    return parsed_names

#example code
if __name__ == "__main__":

    PARSE_LINE = ("DPDHS\n Division  Dengue Fe-\n"+
                  "ver / DHF* Dysentery Encephali\n"+
                  "tis  Enteric\nFever Food\nPoisoning\n"+
                  "  Leptospiro\nsis Typhus\nFever Viral\nHepatitis")
    print(detect_diseases(PARSE_LINE))
