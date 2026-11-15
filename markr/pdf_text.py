from pypdf import PdfReader


def read_pdf(file):
    reader = PdfReader(file)
    text = "\n".join((page.extract_text() or "") for page in reader.pages)
    return text, len(reader.pages)