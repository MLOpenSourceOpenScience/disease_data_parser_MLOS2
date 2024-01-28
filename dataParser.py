import sys
import importlib
from datetime import datetime
import os
from Modules.PDFoperators import *
from Modules.pdfExtractor import *


if __name__ == "__main__":
    
    n = len(sys.argv)
    if n == 2 and sys.argv[1] == "-h": #TODO: improve help dialogue
        print("Usage: dataParser.py <folder-to-parse/> <output-file.csv> <parsing-model>") 
        print("Arg 1: folder of PDFs to parse. They should all be compatible with the same parsing model")
        print("Arg 2: output file, in csv format")
        print("Arg 3: parsing model. PDF will be converted to text, but model will convert text to array data. If it is in a folder, replace / with . in the path so python can import properly")
        quit()
    if (n<4):
        print("Invalid number of arguments! Correct usage: dataParser.py <folder-to-parse> <output-file.csv> <parsing-model.py>")
        print("Example: dataParser.py Data Output/data.csv ParsingModels.sriLankaParser")
        print("run dataParser.py -h for more information")
        quit()
    
    #Import Arguments
    inFolder = sys.argv[1]  # Arg 1: folder of PDFs to parse. They should all be compatible with the same parsing model
    outFile = sys.argv[2]   # Arg 2: output file, in csv format
    modelFile = sys.argv[3] # Arg 3: parsing model. PDF will be converted to text, but model will convert text to array data

    model = importlib.import_module(modelFile) 

    #process each file in input folder
    filesToParse = []
    if os.path.exists(inFolder):
        print("Locating files...")
        for root, dirs, files in os.walk(inFolder):
            for name in files:
                filesToParse.append(name)
    else:
        print(f"ERROR: folder '{inFolder}' not found!")
        quit()
    
    print("Will parse the following files: ",end="")
    for f in filesToParse:
        print(f,end=", ")
    print()
    response = ''
    while response not in ['y','n','yes','no']:
        response = input("Continue? press y/n ").strip().lower()
        if response == 'n' or response == 'no':
            quit()

    for currentFile in filesToParse:
        rtfData = PDFtoRTF(currentFile)
        table = model.extractToTable(rtfData) 

    print(table)


