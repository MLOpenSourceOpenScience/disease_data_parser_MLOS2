"""
Data Parser

Responsible for visualizing the data.
works for weekly as default.

Author: MLOS^2_NLP_TEAM
Date: 2024.04.02
"""

import sys
import csv
import matplotlib.pyplot as plt


def save_to_png(region: str, disease: str, time_base: str, filename: str, timeblock: str, merge: bool = False) -> int:
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
                    if row[1] == '1+Q':
                        row[1] = '1'
                    elif row[1] == 'v':
                        row[1] = '0'
                    year_slot[row[8][7:11]].append(int(row[1]))

        if merge:
            plt.figure()
            plt.title(region+' '+disease)

        for key, datas in year_slot.items():
            if not merge:
                plt.figure()
                plt.title(key+' '+region+' '+disease)
            plt.xlabel(timeblock)
            plt.ylabel('# of cases')

            plt.plot(range(1, len(datas)+1), datas)
            if not merge:
                plt.savefig('Out/'+key + '_' + region +
                            '_' + disease + '.png', dpi=300)
                plt.close()

        if merge:
            plt.legend(year_slot.keys(), loc="center left",
                       bbox_to_anchor=(1, 0.5))
            plt.savefig('Out/'+region+'_'+disease+'.png',
                        bbox_inches="tight", dpi=300)
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
                    year_month_slot[row[8][7:11]+row[8]
                                    [3:6]].append(int(row[1]))
        if merge:
            plt.figure()
            plt.title(region+' '+disease)

        for key, datas in year_month_slot.items():
            if not merge:
                plt.figure()
                plt.title(key+' '+region+' '+disease)
            plt.xlabel(timeblock)
            plt.ylabel('# of cases')

            plt.plot(range(1, len(datas)+1), datas)
            if not merge:
                plt.savefig('Out/'+key + '_' + region +
                            '_' + disease + '.png', dpi=300)
                plt.close()

        if merge:
            plt.savefig('Out/'+region+'_'+disease+'.png', dpi=300)
            plt.close()

    elif time_base == 'fully':
        data = []

        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                sv = row[1].replace('.', '')
                data.append(int(sv))

        plt.figure()
        plt.title(region+' '+disease)
        plt.xlabel(timeblock)
        plt.ylabel('# of cases')
        plt.plot(range(1, len(data)+1), data)
        plt.savefig('Out/'+region + '_' + disease + '.png', dpi=300)
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
        print("\t-b: -b <day/daily/week/weekly> (default is 'week')")
        print("For more specific info, please do -flag -h.")
        sys.exit()

    flag_types = ['-t', '-d', '-r', '-c', ' -b', '-m']
    # -t: time base, 'yearly', 'monthly'
    # -d: DISEASE name
    # -r: region name
    # -c: country code
    # -b: given data block
    # -m: merge into one

    country_mode = '-c' in flags
    region_mode = '-r' in flags
    disease_mode = '-d' in flags
    merge_mode = '-m' in flags

    DATA_SIZE = 'Weeks'

    TIME_BASE = 'yearly'
    if '-t' in flags:
        temp_index = flags.index('-t') + 1
        if temp_index < len(flags) and flags[temp_index] not in flag_types:
            TIME_BASE = flags[temp_index]
            if TIME_BASE == '-h':
                print("-t defines the time series of the graph will be.")
                print(
                    "If you want to see your data as a yearly scale, then input <-t yearly>.")
                sys.exit()
            elif TIME_BASE == 'year':
                TIME_BASE = 'yearly'
            elif TIME_BASE == 'month':
                TIME_BASE = 'monthly'
            elif TIME_BASE == 'full':
                TIME_BASE = 'fully'
                if merge_mode:
                    print("-m not working on full mode")
                    sys.exit()
        else:
            print("Invalid usage of flag '-t'!")
            print("Correct usage: <arguments> -t <year/yearly/month/monthly/full/fully>")
            sys.exit()

    if '-b' in flags:
        temp_index = flags.index('-b') + 1
        if temp_index < len(flags) and flags[temp_index] not in flag_types:
            if flags[temp_index] == '-h':
                print("-b defines what data block is inputed.")
                print("If *.csv's data is given weekly, then do <-b week>.")
                sys.exit()
            if flags[temp_index] in ['week', 'weekly']:
                DATA_SIZE = 'Weeks'
            elif flags[temp_index] in ['day', 'daily']:
                DATA_SIZE = 'Days'
        else:
            print("Invalid usage of flag '-b'!")
            print("Correct usage: <arguments> -t <week/weekly/day/daily>")
            sys.exit()

    DISEASE = 'all'
    if disease_mode:
        temp_index = flags.index('-d') + 1
        if temp_index < len(flags) and flags[temp_index] not in flag_types:
            DISEASE = flags[temp_index]
            if DISEASE == '-h':
                print("-d defines the specific disease that you are interested to see.")
                print("If you want to see Dengue, please input <-d Dengue>.")
                sys.exit()
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
            if REGION == '-h':
                print("-r defines the region that you want to see.")
                print("If you want to see 'Trincomalee', then input <-r trincomalee>.")
        else:
            print("Invalid usage of flag '-r'!")
            print("Correct usage: <arguments> -d <name of the region>")
            sys.exit()

    from Modules.location_interface import get_location_info
    region_long, region_lat, _, _, _ = get_location_info(REGION)

    if region_mode:
        extract_data(region_long, temp_file, temp_file)

    if REGION != 'all' and DISEASE != 'all':
        SUCCESS = save_to_png(REGION, DISEASE, TIME_BASE,
                              temp_file, DATA_SIZE, merge=merge_mode)
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
            SUCCESS = save_to_png(reg, DISEASE, TIME_BASE,
                                  new_temp_file, DATA_SIZE, merge=merge_mode)

            if SUCCESS != 0:
                print("Error Occured")
                sys.exit()
    elif REGION != 'all' and DISEASE == 'all':
        diseases = []
        with open(temp_file, 'r', encoding='utf-8') as target_file:
            readers = csv.reader(target_file)
            next(readers)

            for r in readers:
                if not r[0] in diseases:
                    diseases.append(r[0])

        for dis in diseases:
            new_temp_file = temp_file.split('.')[0] + '_temp.csv'

            extract_data(dis, temp_file, new_temp_file)
            SUCCESS = save_to_png(REGION, dis, TIME_BASE,
                                  new_temp_file, DATA_SIZE, merge=merge_mode)

            if SUCCESS != 0:
                print("Error Occured")
                sys.exit()
