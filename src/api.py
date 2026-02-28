from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel
from retrieve import *
from generate import *
import chromadb
import os
from fastapi import UploadFile, File, Form
import tempfile
from ingest import *

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'db')

class QueryRequest(BaseModel):
    question: str
    drug_filter: list = None
    section_filter: str = None

class QueryResponse(BaseModel):
    answer: str
    sources: list
@asynccontextmanager
async def lifespan(app: FastAPI):
    # runs once at startup
    yield
    # runs once at shutdown

app = FastAPI(lifespan=lifespan)


@app.post("/query",response_model=QueryResponse)
async def query_drugs(request: QueryRequest):
    results = retrieve(request.question, request.drug_filter, request.section_filter)
    answer = generate_answer(request.question, results)
    sources = [f"{m['drug']} - {m['section']}" for m in results['metadatas'][0]]
    return QueryResponse(answer=answer,sources=sources)


@app.get("/drugs")
async def get_drugs():
    client = chromadb.PersistentClient(path=DB_PATH)
    collection = client.get_collection("drug_labels")
    results = collection.get()
    drugs = list(set(m['drug'] for m in results['metadatas']))
    return {"drugs": sorted(drugs)}


@app.post("/ingest")
async def ingest_drug(file: UploadFile = File(...), drug_name: str = Form(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name
    
    chunks = parse_pdf(tmp_path, drug_name)
    embeddings = embed_chunks(chunks)
    store_chunks(chunks, embeddings)
    
    return {"message": f"Successfully ingested {drug_name}", "chunks": len(chunks)}