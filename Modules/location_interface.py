"""
Location Interface

Currentely only supports searching a location
and return the required data to another file.

Importing new data will be supported later on
through this module.

Dependency:
- pip install requests

Author: MLOS^2_NLP_TEAM
Date: 2024.02.05
"""

import csv
import os
from typing import List
import requests

def parse_alpha_only(input_string: str) -> str:
    """
    Read string, and only remain alphanumeric characters, and delete everything else

    Parameters:
    - input_string (str): string that needs to be parsed.

    Return:
    - str: string that is parsed.
    """
    return ''.join(char for char in input_string if char.isalnum() or char in [' ', ','])

API_KEY = 'rgb1WNEXC27GO3f_n6OZzfOCOfHPGiQBPEt2TY0tRhA'

def get_location_info(search_location_original: str, api: str = API_KEY) -> List[int]:
    """
    get the name of the location, and returns Longtitude and Latitude
    Also stores the information including type of the region,
    boundary of the region, and the country code on the dictionary
    LongLatDict.csv

    Parameters:
    - search_location_original (str): The name of the location.
    - api (str): The api value of HERE.com.

    Returns:
    - List[int]: Longtitude, Latitude, Region Type, Country, boundary
    """

    country_consistency = ""

    # remove irrelevant characters
    search_location = parse_alpha_only(search_location_original)
    # even before searching, change word into lowercases (for efficiency)
    search_location = search_location.lower()

    current_directory = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(current_directory, 'LongLatDict.csv')

    with open(file_path, 'r', encoding='utf-8') as file:

        reader = csv.reader(file)

        for row in reader:
            if row and row[0] == search_location:
                if country_consistency == "":
                    country_consistency = row[2]
                elif not country_consistency == row[2]:
                    print("Error: country inconsistency detected."
                          +f"{search_location_original} not found in {country_consistency}")
                    raise ValueError

                return [row[3], row[4], row[1], row[2], row[5]]

    url = "https://geocode.search.hereapi.com/v1/geocode"
    # first tried to use Google API, but it is clearly paid, so found another one.
    ## I'm sure it is working, but I need to figure out the license and usage is permitted.

    params = {
        'limit': 2,
        'q': search_location,
        'apiKey': api
    }

    response = requests.get(url, params= params, timeout= None)
    # parse with response.json
    # has several parameters:
    ## title, id, resultType, localityType,
    ## address, position, access, distance,
    ## categories, references, contacts...
    ## (for more info, seach HERE)

    if response.status_code == 200:
        data = response.json()
        # call it with json()

        if 'items' in data and data['items']:
            location = data['items'][0]
            # 'item' will have only 1 data, so don't go over [1]...and so on.

            region_type = location.get('resultType')
            region_name = location.get(region_type+'Type')
            # what type of region? city, state...

            address = location.get('address', {})
            country_code = address.get('countryCode')
            # code of the country

            if country_consistency == "":
                country_consistency = country_code
            elif not country_consistency == country_code:
                print("Error: country inconsistency detected."
                      +f"{search_location_original} not found in {country_consistency}")

            region_map = location.get('mapView', {})
            # will hold the value of longlat, but as a box-shaped.
            ## leftmost, rightmost, upmost, undermost longlats (4 numbers)

            position = location.get('position', {})
            latitude = position.get('lat')
            longitude = position.get('lng')
            # position will hold only two value, lat and long.

            row = [search_location, region_name, country_code, longitude, latitude, region_map]
            # build row here

            if latitude is not None and longitude is not None:
                with open(file_path, 'a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(row)

                return [longitude, latitude, region_name, country_code, region_map]

            print("Latitude or Longitude not found in the response.")
        else:
            print("No items found in the response.")
    else:
        print(f"Error: {response.status_code}, {response.text}")

    print(f"Error: Location lookup error. Program cannot find {search_location_original}")
    #quit() removed so other functions can continue
    raise ValueError

### example code

if __name__ == '__main__':
    NAME = 'matale, sri lanka'

    long, lat, a, b, c = get_location_info(NAME)

    print (long, lat, a, b, c)
