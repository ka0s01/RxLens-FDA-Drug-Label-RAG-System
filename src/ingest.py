import pdfplumber
import re
SECTIONS = [
    "INDICATIONS AND USAGE",
    "DOSAGE AND ADMINISTRATION",
    "DOSAGE FORMS AND STRENGTHS",
    "CONTRAINDICATIONS",
    "WARNINGS AND PRECAUTIONS",
    "ADVERSE REACTIONS",
    "DRUG INTERACTIONS",
    "USE IN SPECIFIC POPULATIONS",
]
def extract_text_by_page(pdf_path):
    pages=[]
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text_simple(x_tolerance=3, y_tolerance=3)
            if text:
                pages.append(text)
    return pages

def parse_section(pages):
    full_text = "\n".join(pages)
    sections = {}
    current_section = None
    for line in full_text.split("\n"):
        clean = line.strip()
        if not clean:
            continue

        normalized = re.sub(r'^\d+\s+','',clean)

        if normalized in SECTIONS and clean.isupper():
            current_section = normalized
            sections[current_section] = ""
        elif current_section:
            sections[current_section] += clean

    return sections


pages = extract_text_by_page("data/pdfs/warfarin.pdf")
d = parse_section(pages)
print(d.keys())
print(d["CONTRAINDICATIONS"][:300])
