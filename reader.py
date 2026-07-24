def extract_text(doc):

    text = ""

    # Read paragraphs
    for para in doc.paragraphs:
        if para.text.strip():
            text += para.text + "\n"

    # Read tables
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                if cell.text.strip():
                    text += cell.text + "\n"

    return text