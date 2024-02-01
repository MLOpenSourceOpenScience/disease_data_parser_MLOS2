
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

    currentDirectory = os.path.dirname(os.path.realpath(__file__))
    filePath = os.path.join(currentDirectory, 'DiseaseDict.csv')

    names = line.lower().split()

    parsedNames = []

    doubleLength = False
    # flag for two-combined words

    for i in range(0, len(names)):
        if doubleLength:
            doubleLength = False
        else:
            with open(filePath, 'r') as file:

                reader = csv.reader(file)
                nameFound = False
                # for efficiency, if found, will break.

                for row in reader:

                    if nameFound:
                        break
                    if i+1 < len(names) and row and row[0] == names[i]+' '+names[i+1]:
                        # check whether it is two-word combination before going through
                        parsedNames.append(row[1])
                        doubleLength = True
                        nameFound = True
                    elif row and row[0] == names[i]:
                        if row[1] == "ignore":
                            # such as RDHS (location column), WRCD (time and percentage column), or headers that does not have disease data in it.
                            pass
                        else:
                            parsedNames.append(row[1])
                        nameFound = True

                if not nameFound:
                    # for now, append non-sence, but later I will make this to import new words into library
                    parsedNames.append('Error detected with name: {}. Please check the dictionary'.format(names[i]))

    return parsedNames

#example code
if __name__ == "__main__":

    parseLine = "RDHS Dengue Fever Dysentery Encephaliti Enteric Fever Food Poi- Leptospirosis Typhus Viral Hep- Human Chickenpox Meningitis Leishmania- WRCD"

    print(detectDiseases(parseLine))