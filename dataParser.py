import sys
import importlib
import os
import traceback
from Modules.PDFoperators import *
from Modules.pdf_extractor import pdf_to_rtf
from Modules.table_to_csv import print_to_csv



if __name__ == "__main__":

    n = len(sys.argv)
    if n == 2 and sys.argv[1] == "-h": #TODO: improve help dialogue
        print("Usage: dataParser.py <folder-to-parse/> <output-file.csv> <parsing-model>")
        print("Arg 1: folder of PDFs to parse. They should all be compatible with the same parsing model")
        print("Arg 2: output file, in csv format")
        print("Arg 3: parsing model. PDF will be converted to text, but model will convert text to array data. If it is in a folder, replace / with . in the path so python can import properly")
        print("Example: dataParser.py Data Output/data.csv ParsingModels.sriLankaParser")
        print()
        print("Flags:")
        print("-q: Quiet Mode. No stack trace outputs for errors")
        print("-d: Debug Mode. Print inputs to each function")
        quit()
    if n < 4:
        print("Invalid number of arguments! Correct usage: dataParser.py <folder-to-parse> <output-file.csv> <parsing-model.py>")
        print("Example: dataParser.py Data Output/data.csv ParsingModels.sriLankaParser")
        print("run dataParser.py -h for more information")
        quit()

    #Import Arguments
    inFolder = sys.argv[1]  # Arg 1: folder of PDFs to parse. They should all be compatible with the same parsing model
    outFile = sys.argv[2]   # Arg 2: output file, in csv format (only the name of the file)
    modelFile = sys.argv[3] # Arg 3: parsing model. PDF will be converted to text, but model will convert text to array data
    flags = sys.argv[4:]

    quiet_mode = '-q' in flags
    debug_mode = '-d' in flags

    model = importlib.import_module(modelFile) 

    #process each file in input folder
    filesToParse = []
    if os.path.exists(inFolder):
        print("Locating files...")
        for root, dirs, files in os.walk(inFolder):
            for name in files:
                #print(f'root: {root} dirs: {dirs} files: {files}')
                if name[-4:] == '.pdf': # Only parse pdf files
                    filesToParse.append(f'{root}/{name}'.replace('\\', '/'))
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

    i = 1
    for currentFile in filesToParse:
        print(f"Parsing file {i}/{len(filesToParse)}:",currentFile)
        step = 0
        try:
            rtfData = pdf_to_rtf(currentFile)
            step +=1
            table,heading = model.extract_to_table(rtfData, flags = flags)
            for n in range(len(table)):
                table[n].append(currentFile)  # Added file source to show here the data came from
            heading.append("Source File")
            step += 1
            print_to_csv(table,heading,file_name=outFile)
        except Exception as error:
            print(f"Error for file {currentFile} ", end="")
            match step:
                case 0:
                    print("at pdf_to_rtf(). Perhaps the file is not a proper PDF?")
                case 1:
                    print("at model.extract_to_table(). Perhaps you chose the wrong model or have an error in the model?")
                case 2:
                    print("at print_to_csv()")
            if not quiet_mode: 
                traceback.print_exc() # show error stack trace 

        i += 1

    print("Done! Output in", outFile)
