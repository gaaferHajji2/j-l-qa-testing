from PyPDF2 import PdfReader, PdfWriter

reader = PdfReader('file-01.pdf')
writer = PdfWriter()
writer.add_page(reader.pages[0]);
with open('file-03.pdf', 'wb') as f:
    writer.write(f)