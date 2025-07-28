import fitz

def extract_outline_and_sections(pdf_path):
    doc = fitz.open(pdf_path)
    outline = doc.get_toc()
    sections = []
    for item in outline:
        _, title, page = item[:3]
        page_text = doc.load_page(page-1).get_text().strip()
        sections.append({
            "title": title,
            "page": page,
            "text": page_text
        })
    return outline, sections