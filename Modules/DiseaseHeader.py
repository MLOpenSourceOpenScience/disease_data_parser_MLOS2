
import os
import csv

def detectDiseases(line: str) -> list[str]:
    """
    Read line, ans seprate the diseases by names.

    Parameters:
    - line (str): The list of names, seperated by space.

    Returns:
    - list[str]: names of diseases parsed
    """

    current_directory = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(current_directory, 'DiseaseDict.csv')

    names = line.lower().split()

    parsed_names = []

    double_length = False
    # flag for two-combined words

    for i in range(0, len(names)):
        if double_length:
            double_length = False
        else:
            with open(file_path, 'r') as file:

                reader = csv.reader(file)
                name_found = False
                # for efficiency, if found, will break.

                for row in reader:

                    if name_found:
                        break
                    if i+1 < len(names) and row and row[0] == names[i]+' '+names[i+1]:
                        # check whether it is two-word combination before going through
                        parsed_names.append(row[1])
                        double_length = True
                        name_found = True
                    elif row and row[0] == names[i]:
                        if row[1] == "ignore":
                            # such as RDHS (location column), WRCD (time and percentage column), or headers that does not have disease data in it.
                            pass
                        else:
                            parsed_names.append(row[1])
                        name_found = True

                if not name_found:
                    # for now, append non-sence, but later I will make this to import new words into library
                    parsed_names.append('Error detected with name: {}. Please check the dictionary'.format(names[i]))

    return parsed_names

#example code
if __name__ == "__main__":

    PARSE_LINE = "RDHS Dengue Fever Dysentery Encephaliti Enteric Fever Food Poi- Leptospirosis Typhus Viral Hep- Human Chickenpox Meningitis Leishmania- WRCD"

    print(detectDiseases(PARSE_LINE))
