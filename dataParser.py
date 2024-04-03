"""
Data Parser

Responsible for getting command line arguments and do the
job as assigned. It will send correct data and command to
whatever the fuction which handles the job.

Author: MLOS^2_NLP_TEAM
Date: 2024.02.09
"""

import sys
import importlib
import os
import traceback
import shutil
import ntpath
# from Modules.PDFoperators import *
from Modules.pdf_extractor import pdf_to_rtf
from Modules.table_to_csv import print_to_csv
from Modules.file_functions import make_valid_filename



if __name__ == "__main__":

    n = len(sys.argv)
    if n == 2 and sys.argv[1] == "-h": #TODO: improve help dialogue
        print("Usage: dataParser.py <folder-to-parse/> <output-file.csv> <parsing-model>")
        print("Arg 1: folder of PDFs to parse. "
              +"They should all be compatible with the same parsing model")
        print("Arg 2: output file, in csv format")
        print("Arg 3: parsing model. "+
              "PDF will be converted to text, but model will convert text to array data. "
              +"If it is in a folder, replace / with . in the path so python can import properly")
        print("Example: dataParser.py Data Output/data.csv ParsingModels.sriLankaParser")
        print()
        print("Flags:")
        print("-q: Quiet Mode. No stack trace outputs for errors")
        print("-d: Debug Mode. Print inputs to each function")
        print("-l [Path/To/File]: Logs all failed pdfs to file, for debugging")
        print("-s keyword [Path/To/File]: Extracts data that contains keywords.")
        print("-errordir [Path/To/Directory]: Copies all failed pdfs into directory, for debugging")
        quit()
    if n < 4:
        print("Invalid number of arguments! Correct usage: "
              +"dataParser.py <folder-to-parse> <output-file.csv> <parsing-model.py>")
        print("Example: dataParser.py Data Output/data.csv ParsingModels.sriLankaParser")
        print("run dataParser.py -h for more information")
        sys.exit()

    #Import Arguments
    inFolder = sys.argv[1]
    # Arg 1: folder of PDFs to parse. They should all be compatible with the same parsing model
    outFile = sys.argv[2]
    # Arg 2: output file, in csv format (only the name of the file)
    modelFile = sys.argv[3]
    # Arg 3: parsing model. PDF will be converted to text, but model will convert text to array data
    flags = sys.argv[4:]

    flag_types = ['-q','-d','-l','-s','-asc','-desc','-errordir']

    quiet_mode = '-q' in flags
    debug_mode = '-d' in flags
    log_mode = '-l' in flags
    extract_mode = '-s' in flags
    error_dir_mode = '-errordir' in flags
    sort_mode = '-asc' in flags or '-desc' in flags
    LOG_FILE_PATH = None
    ERROR_DIR = None

    # Log Mode
    if log_mode:
        try:
            log_filename = flags[flags.index('-l')+1]
            if log_filename in flag_types:
                # If the value after -o is just another flag and not a log file
                raise SyntaxError
        except:
            print("Error with -l flag: Can't find path to log file. "
                  +"Proper usage: -l [Path/To/File]")
            sys.exit()
        LOG_FILE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), log_filename)
        log_directory = os.path.dirname(LOG_FILE_PATH)
        if not os.path.exists(log_directory): # If there is no directory, make it
            os.makedirs(log_directory)

    #Error Dir Mode
    if error_dir_mode:
        try:
            err_dir = flags[flags.index('-errordir')+1]
            if err_dir in flag_types:
                # If the value after -errordir is just another flag and not a log file
                raise SyntaxError
        except:
            print("Error with -errordir flag: Can't find path to error directory. "
                  +"Proper usage: -errordir [Path/To/Directory]")
            sys.exit()
        ERROR_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), err_dir)
        if not os.path.exists(ERROR_DIR): # If there is no directory, make it
            os.makedirs(ERROR_DIR)

    model = importlib.import_module(modelFile)

    #process each file in input folder
    filesToParse = []
    if os.path.exists(inFolder):
        print("Locating files...")
        for root, dirs, files in os.walk(inFolder):
            for name in files:
                #print(f'root: {root} dirs: {dirs} files: {files}')
                if name[-4:] == '.pdf' or name[-4:] == '.txt': # Only parse pdf or txt files
                    filesToParse.append(f'{root}/{name}'.replace('\\', '/'))
    else:
        print(f"ERROR: folder '{inFolder}' not found!")
        quit()

    print("Will parse the following files: ",end="")
    for f in filesToParse:
        print(f,end=", ")
    print()
    RESPONSE = ''
    while RESPONSE not in ['y','n','yes','no']:
        RESPONSE = input("Continue? press y/n ").strip().lower()
        if RESPONSE in ['n', 'no']:
            sys.exit()

    i = 1
    NUM_ERRORS = 0
    for currentFile in filesToParse:
        print(f"Parsing file {i}/{len(filesToParse)}:",currentFile)
        STEP = 0
        try:
            rtfData = []
            if currentFile[-4:] == '.pdf': #if file is PDF
                rtfData = pdf_to_rtf(currentFile)
            elif currentFile[-4:] == '.txt': #if file is txt
                with open(currentFile) as txt_data:
                    rtfData = [txt_data.read()]
            STEP +=1
            table,heading = model.extract_to_table(rtfData, flags = flags)
            for n in range(len(table)):
                table[n].append(currentFile)  # Added file source to show here the data came from
            heading.append("Source File")
            STEP += 1
            print_to_csv(table,heading,file_name=outFile)
        except Exception as error:
            NUM_ERRORS += 1
            error_message = f"Error for file {currentFile} "

            match STEP:
                case 0:
                    error_message += "at pdf_to_rtf(). Perhaps the file is not a proper PDF?\n"
                case 1:
                    error_message += ("at model.extract_to_table(). "
                                      +"Perhaps you chose the wrong model "
                                      +"or have an error in the model?\n")
                case 2:
                    error_message += "at print_to_csv()\n"
            print(error_message)
            if not quiet_mode:
                traceback.print_exc() # show error stack trace
            if log_mode: # Log error in logfile
                with open(LOG_FILE_PATH, 'a', encoding= 'utf-8') as log_file:
                    log_file.write(error_message)
                    log_file.write(traceback.format_exc())
                    log_file.write('\n')
            if error_dir_mode: # Place error files into new directory
                error_folder = traceback.format_exc().split('\n')[-4]
                start_of_folder_name = error_folder.rfind("line")
                if start_of_folder_name == -1:
                    #can't find line, can't categorize error (shouldn't happen)
                    print("can't find line in:", error_folder)
                    shutil.copy(currentFile, os.path.join(ERROR_DIR, ntpath.basename(currentFile)))
                else:
                    error_folder = error_folder[start_of_folder_name:]
                    error_folder = make_valid_filename(error_folder)
                    output_dir = os.path.join(ERROR_DIR, error_folder)
                    if not os.path.exists(output_dir): # If there is no directory, make it
                        os.makedirs(output_dir)
                    shutil.copy(currentFile, os.path.join(output_dir, ntpath.basename(currentFile)))


        i += 1

    print("Done! Output in", outFile)
    print(f"There were errors in {NUM_ERRORS}/{len(filesToParse)} files")
    if log_mode:
        with open(LOG_FILE_PATH, 'a', encoding= 'utf-8') as log_file:
            log_file.write(f"There were errors in {NUM_ERRORS}/{len(filesToParse)} files")

    if sort_mode:
        from Modules.csv_management import order_by_time

        if '-asc' in flags:
            order_by_time(outFile)
        elif '-desc' in flags:
            order_by_time(outFile, asc= False)

    if extract_mode:
        try:
            target_keyword = flags[flags.index('-s') + 1]
            if target_keyword in flag_types:
                raise SyntaxError
        except SyntaxError:
            print("Error with -s flag: Can't find proper keyword"
                  +"Proper usage: -s keyword [Path/To/File]")
            sys.exit()

        OUTPUT_PATH = None

        path_index = flags.index('-s') + 2

        if path_index < len(flags):
            temp_path = flags[path_index]
            if temp_path not in flag_types:
                OUTPUT_PATH = temp_path

        if OUTPUT_PATH is None:
            OUTPUT_PATH = outFile.split('.')[0] + '_' + target_keyword + '.csv'

        from Modules.csv_management import extract_data

        extract_data(target_keyword, outFile, OUTPUT_PATH)

