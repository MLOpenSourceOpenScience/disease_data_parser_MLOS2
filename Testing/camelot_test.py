import camelot
import os


filePath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sri lanka.pdf")

abc = camelot.read_pdf(filePath)
print(abc[0].df)
