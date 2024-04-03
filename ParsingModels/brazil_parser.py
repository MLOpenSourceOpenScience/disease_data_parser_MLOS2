"""
Brazil Parser

Author: MLOS^2_NLP_TEAM
Date: 2024.02.26
"""

import os
import sys
from typing import List

current_directory = os.path.dirname(__file__)
moudlues_directory = os.path.join(current_directory, '../Modules')
sys.path.append(moudlues_directory)

from ParsingModels.BrazilModules.brazil_convert_to_table import convert_to_table, tableHeading
from table_conversion_functions import print_table


def extract_to_table(rtf_data: List[str], flags: List[str] = None) -> [List[List[str]], List[str]]:
    """
    Get rtf data with flag and translate into 2D array (table)
    with Header.

    Supports various option if flag is on.

    Prarmeters:
    - rtf_data (List[str]): Data in rtf format.
    - flags (List[str]): Flag for options, such as debugging.

    Returns:
    - [List[List[str]], List[str]]: Table data, Header.
    """
    if flags is None:
        debug_mode = False
    else:
        debug_mode = '-d' in flags
    if debug_mode:
        print("DEBUG - Raw Text Data:")
        print(rtf_data)

    #Hard coded, can be made to be an argument
    disease_name = "Dengue Fever"

    table, heading = convert_to_table(rtf_data, disease_name = disease_name, flags = flags)

    if debug_mode:
        print("DEBUG - Output Table:")
        print_table(table, heading)

    return table, heading
