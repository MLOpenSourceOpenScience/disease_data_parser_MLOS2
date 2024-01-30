#Alan

import subprocess as sp
import pathlib
import os

def PDFtoRTF(path, output_file=None):
    #Generate a text rendering of a PDF file in the form of a list of lines.
    if output_file is None:
        args = ['pdftotext', '-layout', path]
    else:
        args = ['pdftotext', '-layout', path, output_file]
    cp = sp.run(
      args, stdout=sp.PIPE, stderr=sp.DEVNULL,
      check=True, text=True
    )
    return cp.stdout

def runner():
    this_path = os.getcwd()
    this_path = this_path[:this_path.rfind('\\')]
    input_file = this_path + '\\Data\\Dengue\\sri lanka.pdf'
    print(input_file)
    output_name = input_file[input_file.rfind('\\') + 1:]
    pathlib.Path('PDFAsText').mkdir(parents=True, exist_ok=True)
    print(PDFtoRTF(input_file))
    #print(PDFtoRTF(input_file, f'PDFAsText/{output_name}.txt'))

if __name__ == '__main__':
    runner()