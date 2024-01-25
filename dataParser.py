import sys
import importlib;
from datetime import datetime;
from Modules.PDFoperators import *


if __name__ == "__main__":
    
    n = len(sys.argv)
    if n == 2 and sys.argv[1] == "-h": #TODO: improve help options
        print("Usage: dataParser.py <folder-to-parse/> <output-file.csv> <parsing-model.py>") 
        print("Arg 1: folder of PDFs to parse. They should all be compatible with the same parsing model")
        print("Arg 2: output file, in csv format")
        print("Arg 3: parsing model. PDF will be converted to text, but model will convert text to array data. If it is in a folder, replace / with . in the path so python can import properly")
        quit()
    if (n<4):
        print("Invalid number of arguments! Correct usage: dataParser.py <folder-to-parse/> <output-file.csv> <parsing-model.py>")
        print("Example: dataParser.py Data Output/data.csv ParsingModels.sriLankaParser.py")
        print("run dataParser.py -h for more information")
        quit()
    
    #Import Arguments
    inFolder = sys.argv[1]  # Arg 1: folder of PDFs to parse. They should all be compatible with the same parsing model
    outFile = sys.argv[2]   # Arg 2: output file, in csv format
    modelFile = sys.argv[3] # Arg 3: parsing model. PDF will be converted to text, but model will convert text to array data

    model = importlib.import_module(modelFile) 

    #formattedPDF = formatPDF(filename) #Alan
    #rtfData = PDFtoRTF(formattedPDF) #Alan
    rtfData = "ahhhh"
    importantText,timestamps = model.extractDataFromRTF(rtfData) #Eoin
    table = model.convertToTable(importantText,timestamps) #Mahi

    print(table)


