'''
Extract target data from csv file

This model will be responsible for extracting the data for user's need,
such as data of a single diseases, or single location.

Author: MLOS^2_NLP_TEAM
Date: 2024.02.06
'''

import os
from typing import Tuple

def source_control(input_file: str, output_file: str) -> Tuple(os.path, os.path):
    '''
    Reads two strgin, and creats path if it is unavailable yet.
    
    Then, return two paths.

    Parameters:
    - input_file (str): Location of an input file.
    - ouput_file (str): Location of an output file.

    Returns:
    - os.path: path of an input file.
    - os.path: path of an output file.
    '''

    file_path = os.path.join(
        os.path.dirname(os.path.join(os.path.dirname(__file__), '../')),
        input_file
    )

    output_path = os.path.join(
        os.path.dirname(os.path.join(os.path.dirname(__file__), '../')),
        output_file
    )

    output_directory = os.path.dirname(output_path)

    if not os.path.exists(output_directory):
        # if there's no outputfile already, create one.
        os.makedirs(output_directory)


def extract_data(target: str, filename: str = 'Out/output.csv', outfile: str = None) -> None:
    '''
    Extract data using given target.

    This fuction will determine whether the given target is location or
    diseases, or even something else.

    Parameters:
    - filename (str): Location of a csv file.
    - target (str): target that user wants to find.
    - outfile (str): location of an output file, default as 'Out/output+
                     (target string).csv'
    '''

    default_location = 'Out/output_'+target+'.csv'

    if outfile is None:
        outfile = default_location
