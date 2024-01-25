#Alan

import subprocess as sp
import pathlib

def PDFtoRTF(path, output_file):
    #Generate a text rendering of a PDF file in the form of a list of lines.
    args = ['pdftotext', '-layout', path, output_file]
    cp = sp.run(
      args, stdout=sp.PIPE, stderr=sp.DEVNULL,
      check=True, text=True
    )
    return cp.stdout

def runner():
    input_file = 'Data/Dengue/dengue sri lanka.pdf'
    output_name = input_file.split('/')[-1]
    pathlib.Path('PDFAsText').mkdir(parents=True, exist_ok=True) 
    print(PDFtoRTF(input_file, f'PDFAsText/{output_name}.txt'))

if __name__ == '__main__':
    runner()