def extract_text(doc):

    text = ""


    for para in doc.paragraphs:
        if para.text.strip():
            text += para.text + "\n"


    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                if cell.text.strip():
                    text += cell.text + "\n"

    return text