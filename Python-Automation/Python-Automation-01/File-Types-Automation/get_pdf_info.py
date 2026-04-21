from PyPDF2 import PdfReader

pdf = PdfReader('file-01.pdf')
print("Num of pages: ", len(pdf.pages));
print("info: ", pdf.metadata)
with open('test-pdf-02.txt', 'w', encoding='utf-8') as f:
    for page in pdf.pages[:207]:
        text = page.extract_text()
        f.write(text)