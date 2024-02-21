"""
File Function

It is a model which responsible of parsing, copying,
or changing file.

Currently only have deleting unvalid characters from
given string.

Author: MLOS^2_NLP_TEAM
Date: 2024.02.21
"""

def make_valid_filename(file_name: str)-> str:
    """
    Removes invalid character for creating files.

    Parameters:
    - file_name (str): Name of the file.

    Returns:
    - str: Fixed filename.
    """
    #Remove invalid characters from filename
    for c in '#%&\\{\\}\\<>*?/$!\'\":@+`|=,':
        file_name = file_name.replace(c,'')
    return file_name
    #return re.sub('#%&{}\<>*?/$!\'\":@+`|=','', filename)


if __name__ == '__main__':
    FILENAME = 'line 124, in <module>'
    print(make_valid_filename(FILENAME))
