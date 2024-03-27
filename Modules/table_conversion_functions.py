"""
Brazil Parser

Author: MLOS^2_NLP_TEAM
Date: 2024.03.26
"""

from datetime import datetime, timedelta
from typing import List
import re
from dateutil.parser import parse as dateparse


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

# Remove unneccessary data


def remove_quotes(data: str):
    return data.replace('"', '').strip()

# Remove numbers


def remove_numbers(data: str):
    data = re.sub("\d+", "", data)
    return data.strip()


def print_table(tabled_text: List[str], header: List[str]) -> None:
    """
    Read table and print it as formatted output

    Parameters:
    - tabled_text (List[str]): data formatted as table
    """
    for heading in header:
        print(f"|{heading:<15}", end=" ")
    print("|")
    for row in tabled_text:
        for col in row:
            print(f"|{col:<15}", end=" ")
        print("|")


def last_day_of_month(date: datetime) -> datetime:
    # The day 28 exists in every month. 4 days later, it's always next month
    next_month = date.replace(day=28) + timedelta(days=4)
    # subtracting the number of the current day brings us back one month
    return next_month - timedelta(days=next_month.day)


def month_to_timestamps(month: str, year: str) -> List[datetime]:
    # Get start of month to end of month
    month = dateparse(f"{year} {month} 1")
    return [month, last_day_of_month(month)]

# Week number starts at 1


def week_number_to_datetime(week_number: int, year: int, zeroth_week=False) -> datetime:
    return datetime(year, 1, 1) + timedelta(days=7 * (week_number-1))
