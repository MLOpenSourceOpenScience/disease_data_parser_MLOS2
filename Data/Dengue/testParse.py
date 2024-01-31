from PyPDF2 import PdfReader

out = ""
reader = PdfReader('sri lanka.pdf')

for page in reader.pages:
    out += page.extract_text()

print(out)
outFile = open("Output.txt", "w", encoding="utf-8")
print(out, file=outFile)
