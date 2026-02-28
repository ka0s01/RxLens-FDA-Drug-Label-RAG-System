from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel
from retrieve import retrieve
from generate import generate_answer
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

