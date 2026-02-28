import chromadb
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
import os
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'db')

def build_where(drug_filter, section_filter):
    conditions = []
    
    if drug_filter:
        if len(drug_filter) == 1:
            conditions.append({"drug": drug_filter[0]})
        else:
            conditions.append({"$or": [{"drug": d} for d in drug_filter]})
    
    if section_filter:
        conditions.append({"section": section_filter})
    
    if len(conditions) == 0:
        return None
    if len(conditions) == 1:
        return conditions[0]
    return {"$and": conditions}

KNOWN_DRUGS = ["warfarin", "aspirin", "metformin"]

def extract_drug_filter(question):
    question_lower = question.lower()
    found = [drug.capitalize() for drug in KNOWN_DRUGS if drug in question_lower]
    return found if found else None

def retrieve(query, drug_filter=None, section_filter=None, k=8):
    client = chromadb.PersistentClient(path=DB_PATH)
    collection = client.get_collection("drug_labels")
    query_embedding = model.encode([query], device='cuda').tolist()
    
    if not drug_filter:
        drug_filter = extract_drug_filter(query)
    
    where = build_where(drug_filter, section_filter)
    
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=k,
        where=where
    )
    return results