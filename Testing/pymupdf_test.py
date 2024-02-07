import fitz
import os


filePath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "oldformat.pdf")

doc = fitz.open(filePath) 
for page in doc:
  text = page.get_text()
  print(text)