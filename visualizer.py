"""
Data Parser

Responsible for visualizing the data.

Author: MLOS^2_NLP_TEAM
Date: 2024.04.02
"""

import sys
import matplotlib.pyplot as plt

if __name__ == "__main__":

    n = len(sys.argv)
    if n < 2:
        print("Invalid number of arguments! Correct usage: "
              + "visualizer.py <folder-to-data> <arguments>")
        print("Example: visualizer.py Output/data.csv [flags]")
        sys.exit()

    data_file = sys.argv[1]
    flags = sys.argv[2:]

    flag_types = ['-t', '-d', '-r', '-c']
    # -t: time base, 'yearly', 'monthly'
    # -d: DISEASE name
    # -r: region name
    # -c: country code

    country_mode = '-c' in flags
    region_mode = '-r' in flags
    disease_mode = '-d' in flags

    TIME_BASE = 'yearly'
    if '-t' in flags:
        temp_index = flags.index('-t') + 1
        if temp_index < len(flags) and flags[temp_index] not in flag_types:
            TIME_BASE = flags[temp_index]
        else:
            print("Invalid usage of flag '-t'!")
            print("Correct usage: <arguments> -t <year/yearly/month/monthly>")
            sys.exit()

    if TIME_BASE == 'year':
        TIME_BASE = 'yearly'
    elif TIME_BASE == 'month':
        TIME_BASE = 'monthly'

    DISEASE = 'all'
    if disease_mode:
        temp_index = flags.index('-d') + 1
        if temp_index < len(flags) and flags[temp_index] not in flag_types:
            DISEASE = flags[temp_index]
        else:
            print("Invalid usage of flag '-d'!")
            print("Correct usage: <arguments> -d <name of diseases>")
            sys.exit()

    from Modules.disease_header_parser import detect_diseases
    DISEASE = detect_diseases(DISEASE)[0]

    from Modules.csv_management import order_by_time, extract_data

    temp_file = data_file.split('.')[0] + '_temp.csv'
    order_by_time(data_file, temp_file)

    if disease_mode:
        extract_data(DISEASE, temp_file, temp_file)

    REGION = 'all'
    if region_mode:
        temp_index = flags.index('-r') + 1
        if temp_index < len(flags) and flags[temp_index] not in flag_types:
            REGION = flags[temp_index]
        else:
            print("Invalid usage of flag '-r'!")
            print("Correct usage: <arguments> -d <name of the region>")
            sys.exit()

    from Modules.location_interface import get_location_info
    region_long, region_lat, _, _, _ = get_location_info(REGION)

    if region_mode:
        extract_data(region_long, temp_file, temp_file)
