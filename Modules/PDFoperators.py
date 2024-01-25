# rotate PDF

from os import listdir
from PyPDF2 import PdfReader, PdfWriter

input_dir  = "Data/Dengue/"
output_dir = "Data/Dengue/"

def rotate_PDFs(input_dir, output_dir, amount=270):
    for fname in listdir(input_dir):
        if not fname.endswith(".pdf"):  # ignore non-pdf files
            continue
        rotate_PDF(input_dir + fname, output_dir + fname, amount)

def rotate_PDF(input_file, output_file, amount=270):
    reader = PdfReader(input_file)
    writer = PdfWriter()
    for page in reader.pages:
        page.rotate(amount) # clockwise 270d
        writer.add_page(page)
    with open(output_file, "wb") as pdf_out:
        writer.write(pdf_out)

def separate_PDF_page(input_file, output_file, selection):
    reader = PdfReader(input_file)
    writer = PdfWriter()
    counter = 0
    for page in reader.pages:
        counter += 1
        if counter in selection:
            writer.add_page(page)
    with open(output_file, "wb") as pdf_out:
        writer.write(pdf_out)
