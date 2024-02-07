#Alan
"""
PDF Extractor

It reads PDF and convert it to RTF format.

Author: MLOS^2_NLP_TEAM
Date: 2024.02.07
"""

import os
from PyPDF2 import PdfReader

def PDFtoRTF(path: str, output_path: str = None) -> str:
    """
    Reads file path, and get pdf file and read through it.
    After reading it, convert texts and write it as RTF if
    output path exists, otherwise not write it, then return
    the converted strings.

    Parameters:
    - path (str): File path that pdf file exsists.
    - output_path (str): File path that rtf file will created.
        If not given, it is None by default.

    Returns:
    - str: String that is converted from pdf file.
    """
    #Generate a text rendering of a PDF file in the form of a list of lines.
    full_text = ""

    with open(path, 'rb') as f:
        pdf = PdfReader(f)
        for page in pdf.pages:
            text = page.extract_text()
            full_text += f"\n\n{text}"

    # if output file as been specified, save it there
    if output_path is not None:
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(full_text)

    return full_text

def runner():
    input_file = '../Data/Dengue/sri lanka.pdf'
    output_folder = '../Data/Dengue/RTF'
    print(input_file)
    output_file = input_file[input_file.rfind('/') + 1:input_file.rfind('.pdf')] + ".txt"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    print(PDFtoRTF(input_file, f"{output_folder}/{output_file}"))

if __name__ == '__main__':
    runner()
