import sys
import os
from datetime import datetime,timedelta
from typing import List, Optional
import re

current_directory = os.path.dirname(__file__)
moudlues_directory = os.path.join(current_directory, '../../Modules')
sys.path.append(moudlues_directory)
# Gets the directory of Modules for import

from location_interface import get_location_info
from disease_header_parser import detect_diseases

tableHeading = ['Disease Name',
                'Cases',
                'Location Name',
                'Country Code',
                'Region Type',
                'Lattitude',
                'Longitude',
                'Region Boundary',
                'TimeStampStart',
                'TimeStampEnd']


def convert_to_table(important_text: List[str], disease_name: str,
                     flags: List[str] = None) -> List[str]:
    """
    Read text file and parse it, creating a List of string which holds
    the same information as a table format (2D). Will get a timestaps
    as a list of datetime seperately.

    Parameters:
    - important_text (str): Chunk of text file that will be parsed.
    - timestapes (List[datetime]): Two timestamp value (start, end)

    Returns:
    - List[str]: Parsed text in a table format.
    """
    table_values = None
    debug_mode = flags is not None and '-d' in flags

    rows = important_text[0].split('\n')

    year = rows[0]
    source = rows[1]
    header = rows[2].split(';')
    rows = rows[3:]

    print(year)
    print(source)
    print(header)
    print(rows[:4])

    table_data = []

    for r in rows:
        cells = r.split(';')
        location_name = cells[0]
        #long, lat, region_type, country_code, region_boundary = get_location_info(location_name)
        for i in range(2, len(cells)):
            cases = 0 if cells[i] == '-' else cells[i] #if data is -, it is actually zero
            time_label = header[i]
            '''
            table_data.append([disease_name,
                    cases,
                    location_name,
                    country_code,
                    region_type,
                    lat,
                    long,
                    region_boundary,
                    time_label,
                    time_label])
            '''
            table_data.append([disease_name,
                    cases,
                    location_name,
                    time_label,
                    time_label])

    for i in range(4):
        print(table_data[i])

    return table_data