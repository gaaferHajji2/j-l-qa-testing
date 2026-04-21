import pdfminer.high_level as hl

text = hl.extract_text('file-01.pdf', maxpages=3)
with open('test-pdf.txt', 'w', encoding='utf-8') as f:
    print(text)
    f.write(text)