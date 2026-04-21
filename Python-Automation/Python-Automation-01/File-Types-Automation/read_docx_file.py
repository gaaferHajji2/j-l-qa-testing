from docx import Document

t1 = Document("jloka-test-docx.docx")
for p in t1.paragraphs:
    print(p.text)