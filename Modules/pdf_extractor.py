"""
PDF Extractor

It reads PDF and convert it to RTF format.

Dependdncy:
- pip install PyMuPDF
- pip install PyPDF2

Author: MLOS^2_NLP_TEAM
Date: 2024.02.07
"""

import os
from typing import List
from PyPDF2 import PdfReader
import fitz as pymupdf #pymupdf

def pdf_to_rtf(path: str, output_path: str = None) -> List[str]:
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
    - List[str]: 2 strings that is converted from pdf file, index 0 is pypdf2, index 1 is pymupdf.
    """
    #Generate a text rendering of a PDF file in the form of a list of lines.
    full_text_pypdf2 = ""
    full_text_pymupdf = ""

    with open(path, 'rb') as f:
        pdf = PdfReader(f)
        for page in pdf.pages:
            try:
                text = page.extract_text()
            except:
                text = ""
            full_text_pypdf2 += f"\n\n{text}"
        doc = pymupdf.open(f)
        for page in doc:
            text = page.get_text()
            full_text_pymupdf += f"\n\n{text}"

    # if output file has been specified, save it there
    if output_path is not None:
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(full_text_pypdf2)

    return [full_text_pypdf2, full_text_pymupdf]

def runner():
    """
    Testing function for main
    """
    input_file = '../Data/Dengue/sri lanka.pdf'
    output_folder = '../Data/Dengue/RTF'
    print(input_file)
    output_file = input_file[input_file.rfind('/') + 1:input_file.rfind('.pdf')] + ".txt"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    print(pdf_to_rtf(input_file, f"{output_folder}/{output_file}"))

if __name__ == '__main__':
    runner()
