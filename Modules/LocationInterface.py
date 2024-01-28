
import requests
import csv
import os

def getLongLat(searchLocation: str, API: str) -> list[int]:
    """
    get the name of the location, and returns Longtitude and Latitude

    Parameters:
    - searchLocation (str): The name of the location.
    - API (str): The api value of HERE.com.

    Returns:
    - list[int]: Longtitude, Latitude.
    """

    currentDirectory = os.path.dirname(os.path.realpath(__file__))
    filePath = os.path.join(currentDirectory, 'LongLatDict.csv')

    with open(filePath, 'r') as file:

        reader = csv.reader(file)

        for row in reader:
            if row and row[0] == searchLocation:
                return [row[1], row[2]]

    url = "https://geocode.search.hereapi.com/v1/geocode"
    # first tried to use Google API, but it is clearly paid, so found another one.
    ## I'm sure it is working, but I need to figure out the license and usage is permitted.

    params = {
        'limit': 2,
        'q': searchLocation,
        'apiKey': API
    }

    response = requests.get(url, params=params)
    # parse with response.json
    # has several parameters:
    ## title, id, resultType, localityType, address, position, access, distance, categories, references, contacts... (for more info, seach HERE)

    if response.status_code == 200:
        data = response.json()
        
        if 'items' in data and data['items']:
            location = data['items'][0]
            position = location.get('position', {})
            
            latitude = position.get('lat')
            longitude = position.get('lng')
            
            if latitude is not None and longitude is not None:
                with open(filePath, 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([searchLocation, longitude, latitude])

                return [longitude, latitude]
            else:
                print("Latitude or Longitude not found in the response.")
        else:
            print("No items found in the response.")
    else:
        print(f"Error: {response.status_code}, {response.text}")

    return 0

### example code

key = 'rgb1WNEXC27GO3f_n6OZzfOCOfHPGiQBPEt2TY0tRhA'
name = 'Colombo'

long, lat = getLongLat(name, key)

print (long, lat)
