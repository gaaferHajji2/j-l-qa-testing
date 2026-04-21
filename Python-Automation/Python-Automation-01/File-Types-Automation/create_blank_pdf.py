from PyPDF2 import PdfWriter

writer = PdfWriter()
page = writer.add_blank_page(width=500, height=250)
with open('file-02.pdf', 'wb') as f:
    writer.write(f)