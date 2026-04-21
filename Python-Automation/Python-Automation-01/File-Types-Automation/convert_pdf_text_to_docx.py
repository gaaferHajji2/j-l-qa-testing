# Import pdf modules
from PyPDF2 import PdfReader
# Import docx modules
from docx import Document

reader = PdfReader('file-01.pdf')
content = ""
for page in reader.pages:
    content += page.extract_text()

def valid(c):
    codepoint = ord(c)
    # conditions ordered by presumed frequency
    return (
        0x20 <= codepoint <= 0xD7FF or
        codepoint in (0x9, 0xA, 0xD) or
        0xE000 <= codepoint <= 0xFFFD or
        0x10000 <= codepoint <= 0x10FFFF
        )

t1 = ''.join(t2 for t2 in content if valid(t2))
document = Document()
document.add_paragraph(t1)
document.save('jloka-pdf-2-docx.docx')