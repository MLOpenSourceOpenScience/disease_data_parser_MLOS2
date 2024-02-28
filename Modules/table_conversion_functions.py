import sys
import os
from datetime import datetime,timedelta
from typing import List, Optional
import re



def time_to_excel_time(time: datetime) -> str:
    """
    Get time as datetime format, and return str type of that same datetime.

    Parameters:
    - time (datetime): The time given.

    Returns:
    - str: The same time writen as a string.
    """
    return time.strftime("%d-%b-%Y %H:%M:%S")



# Removes blank values from a List
def remove_blank_values(data: List[str]) -> List[str]:
    """
    Removes empty entries in data (such as '')
    Also removes unessacary blank spaces from the strings
    """

    new_data = []

    for row in data:
        new_data.append(row.strip())

    return list(filter(str.strip, new_data))



def print_table(tabled_text: List[str], header: List[str])-> None:
    """
    Read table and print it as formatted output

    Parameters:
    - tabled_text (List[str]): data formatted as table
    """
    for heading in header:
        print(f"|{heading:<15}",end=" ")
    print("|")
    for row in tabled_text:
        for col in row:
            print(f"|{col:<15}",end=" ")
        print("|")