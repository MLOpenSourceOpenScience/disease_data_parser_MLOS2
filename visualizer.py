"""
Data Parser

Responsible for visualizing the data.

Author: MLOS^2_NLP_TEAM
Date: 2024.04.02
"""

import sys
import csv
import matplotlib.pyplot as plt


def save_to_png(region: str, disease: str, time_base: str, filename: str) -> int:
    """
    function that converts specified csv into png file.
    """
    if time_base == 'yearly':
        processed = []
        year_slot = {}
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                if not row[8][7:11] in processed:
                    processed.append(row[8][7:11])
                    year_slot[row[8][7:11]] = [int(row[1])]
                else:
                    year_slot[row[8][7:11]].append(int(row[1]))

        for key, datas in year_slot.items():
            plt.figure()
            plt.title(key+' '+region+' '+disease)
            plt.xlabel('Weeks')
            plt.ylabel('# of diseases')

            plt.plot(range(1, len(datas)+1), datas)
            plt.savefig('Out/'+key + '_' + region + '_' + disease + '.png')
            plt.close()

    elif time_base == 'monthly':
        processed = []
        year_month_slot = {}

        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                if not row[8][7:11]+row[8][3:6] in processed:
                    processed.append(row[8][7:11]+row[8][3:6])
                    year_month_slot[row[8][7:11]+row[8][3:6]] = [int(row[1])]
                else:
                    year_month_slot[row[8][7:11]+row[8][3:6]].append(int(row[1]))

        for key, datas in year_month_slot.items():
            plt.figure()
            plt.title(key+' '+region+' '+disease)
            plt.xlabel('Weeks')
            plt.ylabel('# of diseases')

            plt.plot(range(1, len(datas)+1), datas)
            plt.savefig('Out/'+key + '_' + region + '_' + disease + '.png')
            plt.close()

    elif time_base == 'fully':
        data = []

        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                data.append(int(row[1]))

        plt.figure()
        plt.title(region+' '+disease)
        plt.xlabel('Weeks')
        plt.ylabel('# of diseases')
        plt.plot(range(1, len(data)+1), data)
        plt.savefig('Out/'+region + '_' + disease + '.png')
        plt.close()

    return 0


if __name__ == "__main__":

    n = len(sys.argv)
    if n < 2:
        print("Invalid number of arguments! Correct usage: "
              + "visualizer.py <folder-to-data> <arguments>")
        print("Example: visualizer.py Output/data.csv [flags]")
        print("For more help, use 'python visulaizer.py -h'")
        sys.exit()

    data_file = sys.argv[1]
    flags = sys.argv[2:]

    if data_file == '-h':
        print("visulizer.py is a program that will extract data from csv file, and save it as a graph.")
        print("Usage of visulizer.py:")
        print("python visulizer.py <folder-to-data> <arguments>")
        print("flags:")
        print("\t-h: -h help (this output)")
        print("\t-t: -t <year/yearly/month/monthly/full/fully> (default is yearly)")
        print("\t-d: -d <name-of-disease> (default is 'all')")
        print("\t-r: -r <name-of-region> (default is 'all')")
        sys.exit()

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
            print("Correct usage: <arguments> -t <year/yearly/month/monthly/full/fully>")
            sys.exit()

    if TIME_BASE == 'year':
        TIME_BASE = 'yearly'
    elif TIME_BASE == 'month':
        TIME_BASE = 'monthly'
    elif TIME_BASE == 'full':
        TIME_BASE = 'fully'

    DISEASE = 'all'
    if disease_mode:
        temp_index = flags.index('-d') + 1
        if temp_index < len(flags) and flags[temp_index] not in flag_types:
            DISEASE = flags[temp_index]
        else:
            print("Invalid usage of flag '-d'!")
            print("Correct usage: <arguments> -d <name of diseases>")
            sys.exit()

    if DISEASE != 'all':
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

    if REGION != 'all' and DISEASE != 'all':
        SUCCESS = save_to_png(REGION, DISEASE, TIME_BASE, temp_file)
        if SUCCESS == 0:
            print("File extracted successfully, saved under 'Out/'")
    elif REGION == 'all' and DISEASE != 'all':
        regions = []
        with open(temp_file, 'r', encoding='utf-8') as target_file:
            readers = csv.reader(target_file)
            next(readers)

            for r in readers:
                if not r[2] in regions:
                    regions.append(r[2])

        for reg in regions:
            new_temp_file = temp_file.split('.')[0] + '_temp.csv'

            extract_data(reg, temp_file, new_temp_file)
            SUCCESS = save_to_png(reg, DISEASE, TIME_BASE, new_temp_file)

            if SUCCESS != 0:
                print("Error Occured")
                sys.exit()

    sys.exit()