
import requests


def getLongLat(location, API):
    url = "https://geocode.search.hereapi.com/v1/geocode"
    params = {
        'limit': 2,
        'q': location,
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
                print(f"Latitude: {latitude}, Longitude: {longitude}")
            else:
                print("Latitude or Longitude not found in the response.")
        else:
            print("No items found in the response.")
    else:
        print(f"Error: {response.status_code}, {response.text}")

    return 0

key = 'rgb1WNEXC27GO3f_n6OZzfOCOfHPGiQBPEt2TY0tRhA'
name = 'Colombo'

getLongLat(name, key)
