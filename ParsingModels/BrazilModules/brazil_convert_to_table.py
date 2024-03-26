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
from table_conversion_functions import time_to_excel_time, remove_quotes, remove_numbers, month_to_timestamps, week_number_to_datetime

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


def get_timestamps(cell: str, year: int) -> List[datetime]:
    if "Total" in cell: #Total, so return the year
        return [datetime(year, 1, 1), datetime(year + 1, 1, 1)]
    elif "Semana" in cell:
        # Weekly Data
        # Assumes format 'Semana ##' with ## being 2 digits indicating week number, including leading 0s
        week_number = int(cell[-2:]) # Gets last 2 characters of header
        week = week_number_to_datetime(week_number, year)
        return [week, week + timedelta(days=7)]
    else:
        # if not weekly, must be monthly
        translated_month = translate_month(cell)
        return month_to_timestamps(translated_month, str(year))


def translate_month(month: str) -> str:
    """
    Translates Months from Portugeuse to English
    """
    months = {"jan":"January",
              "fev":"February",
              "mar":"March",
              "abr":"April",
              "mai":"May",
              "jun":"June",
              "jul":"July",
              "ago":"August",
              "set":"September",
              "out":"October",
              "nov":"November",
              "dez":"December"}
    formatted_month = month.lower().strip()
    if formatted_month in months:
        return months[formatted_month]
    else:
        print("ERROR: Could not find month:",formatted_month)
        raise ValueError



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

    year = int(rows[0])
    source = rows[1]
    header = rows[2].split(';')
    rows = rows[3:-1]

    print(year)
    print(source)
    print(header)
    print(rows[:4])

    table_data = []

    for row in rows:
        cells = row.split(';')
        location_name = remove_numbers(remove_quotes(cells[0]))
        if 'MUNICIPIO IGNORADO' in location_name.upper():
            long, lat, region_type, country_code, region_boundary = 'N/A','N/A','N/A','N/A','N/A'
        else:
            long, lat, region_type, country_code, region_boundary = get_location_info(location_name)
        for i in range(2, len(cells)):
            cases = 0 if cells[i] == '-' else cells[i] #if data is -, it is actually zero
            time_label = remove_quotes(header[i])
            timestamps = get_timestamps(time_label, year)
            table_data.append([disease_name,
                    cases,
                    location_name,
                    country_code,
                    region_type,
                    lat,
                    long,
                    region_boundary,
                    time_to_excel_time(timestamps[0]),
                    time_to_excel_time(timestamps[1])])

    for i in range(4):
        print(table_data[i])

    return table_data