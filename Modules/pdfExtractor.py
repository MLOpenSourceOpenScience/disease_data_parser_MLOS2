#Alan
from PyPDF2 import PdfReader
import os
from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

def PDFtoRTF(path, output_path=None):
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

def PDFtoRTF2(path, output_path=None):
    pdfminer_string = StringIO()
    with open(path, "rb") as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr,
                            pdfminer_string,
                            laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
    pdfminer_lines = pdfminer_string.getvalue().splitlines()
    pdfminer_lines = [ln for ln in pdfminer_lines if ln]

    print(f'pdfMiner: {pdfminer_lines}')
    if output_path is not None:
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(''.join(pdfminer_lines))

def runner():
    input_file = '../Data/Dengue/sri lanka page 3.pdf'
    output_folder = '../Data/Dengue/RTF'
    print(input_file)
    output_file = input_file[input_file.rfind('/') + 1:input_file.rfind('.pdf')] + ".txt"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    PDFtoRTF(input_file, f"{output_folder}/{output_file}")

if __name__ == '__main__':
    runner()