import pdfplumber
import re
from sentence_transformers import SentenceTransformer
import chromadb
import os
model = SentenceTransformer('all-MiniLM-L6-v2')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, '..', 'data', 'db')
pdf_dir = os.path.join(BASE_DIR, '..', 'data', 'pdfs')
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

def parse_sections(pages):
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
            sections[current_section] += (clean + "\n")

    return sections

'''
{
    "text": "Warfarin is contraindicated in patients with hemorrhagic tendencies...",
    "drug_name": "Warfarin",
    "section": "CONTRAINDICATIONS",
    "chunk_id": "warfarin_contraindications_0"
}

'''
def chunk_sections(text,drug_name,section,chunk_size=400,overlap=50):
    chunks = []
    start = 0
    while start<len(text):
        end = min(start+chunk_size,len(text))
        if end < len(text):
            last_space = text.rfind(' ', start, end)
            if last_space > start:
                end = last_space
        chunk_text = text[start:end].strip()
        if chunk_text:
            chunks . append({
                "text" : chunk_text,
                "drug_name": drug_name,
                "section": section,
                "chunk_id":f"{drug_name.lower()}_{section.lower().replace(' ','_')}_{len(chunks)}"
            })
        start = end-overlap
        if end == len(text):
            break
    return chunks


def chunk_drug(sections_dict,drug_name):
    chunks = []
    for section in sections_dict:
        chunks.extend(chunk_sections(sections_dict[section],drug_name,section))
    return chunks

def parse_pdf(pdf_path,drug_name):
    pages = extract_text_by_page(pdf_path)
    sections = parse_sections(pages)
    chunks = chunk_drug(sections,drug_name)
    return chunks

def embed_chunks(chunks):
    texts = [
        f"{chunk['drug_name']} | {chunk['section']} | {chunk['text']}"
        for chunk in chunks
    ]
    embeddings = model.encode(texts,device='cuda')
    return embeddings

def store_chunks(chunks,embeddings):
    client = chromadb.PersistentClient(path=DB_PATH)
    collection = client.get_or_create_collection("drug_labels")
    existing = collection.get(ids=[chunks[0]["chunk_id"]])
    if existing["ids"]:
        print("Already stored, skipping.")
        return
    collection.add(
        documents=[chunk["text"] for chunk in chunks],
        embeddings= embeddings.tolist(),
        metadatas=[{"drug":chunk["drug_name"],"section":chunk["section"]}for chunk in chunks],
        ids=[chunk["chunk_id"] for chunk in chunks]
    )
    print(f"Stored {len(chunks)} chunks")





pdf_dir = "./data/pdfs"
if __name__ == "__main__":
    for filename in os.listdir(pdf_dir):
        if filename.endswith(".pdf"):
            drug_name = filename.replace(".pdf", "").capitalize()
            pdf_path = os.path.join(pdf_dir, filename)
            chunks = parse_pdf(pdf_path, drug_name)
            print(f"{drug_name}: {len(chunks)} chunks")
            embeddings = embed_chunks(chunks)
            store_chunks(chunks, embeddings)