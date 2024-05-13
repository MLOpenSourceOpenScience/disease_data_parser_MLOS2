from PyPDF2 import PdfReader

out = ""
reader = PdfReader('sri lanka.pdf')

for page in reader.pages:
    out += page.extract_text()

print(out)
out_file = open("Output.txt", "w", encoding="utf-8")
print(out, file=out_file)
