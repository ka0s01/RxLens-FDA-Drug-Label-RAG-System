import chromadb
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

def retrieve(query, drug_filter=None, section_filter=None, k=8):
    client = chromadb.PersistentClient(path="./data/db")
    collection = client.get_collection("drug_labels")
    query_embedding = model.encode([query], device='cuda').tolist()
    
    if drug_filter and section_filter:
        where = {"$and": [{"drug": drug_filter}, {"section": section_filter}]}
    elif drug_filter:
        where = {"drug": drug_filter}
    elif section_filter:
        where = {"section": section_filter}
    else:
        where = None
    
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=k,
        where=where
    )
    return results


results = retrieve(
    "what are the contraindications for warfarin",
    drug_filter="Warfarin",
    section_filter="CONTRAINDICATIONS"
)
for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
    print(f"[{meta['drug']} - {meta['section']}]")
    print(doc[:150])
    print()