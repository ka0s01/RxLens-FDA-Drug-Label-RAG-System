# RxLens — FDA Drug Label Rag System

RxLens is a local RAG system that answers natural language questions using FDA drug label data.

It extracts structured information from drug label PDFs, indexes it into a vector database, and retrieves grounded, context-aware answers using a local LLM.

This project focuses on building a RAG pipeline from scratch without abstraction frameworks (LangChain) , to understand ingestion, chunking, embeddings, and retrieval behavior.

---

## What RxLens Does

- Parses FDA drug label PDFs
- Extracts specific high-value medical sections
- Splits text into overlapping chunks for semantic retrieval
- Converts text into embeddings using Sentence Transformers
- Stores embeddings in a persistent vector database (ChromaDB)
- Retrieves relevant context based on user queries
- Generates grounded answers using a local LLM (Ollama / Mistral)

---

## Tech Stack

* Frontend: Streamlit
* Backend : FastAPI
* LLM: Mistral (via Ollama)
* Embeddings: SentenceTransformers (`all-MiniLM-L6-v2`)
* Vector DB: ChromaDB 
* PDF Parsing: pdfplumber
* Language: Python

---

## System Architecture

```text
            User Query
                 ↓
           Streamlit UI
                 ↓
            FastAPI API
                 ↓
        Query Processing Layer
                 ↓
         Vector Retrieval (ChromaDB)
                 ↓
        Top-k Relevant Chunks
                 ↓
        LLM (Mistral)
                 ↓
               Answer
```

---
## Preview

### Query
<img width="1869" height="519" alt="image" src="https://github.com/user-attachments/assets/5df4470d-7ab4-47b8-9042-c695ff0ee2d9" />

### Drug Library

<img width="1870" height="887" alt="image" src="https://github.com/user-attachments/assets/42c0b3c5-6dcd-4626-adb3-44710c4dcb71" />

### Add a drug

<img width="1868" height="758" alt="image" src="https://github.com/user-attachments/assets/6456c0d5-6cf9-4e97-a84f-ede16b38207c" />

### Working

<img width="1859" height="770" alt="image" src="https://github.com/user-attachments/assets/01a45003-2db7-4fd3-9a06-7fa1916b684b" />
<img width="1871" height="565" alt="image" src="https://github.com/user-attachments/assets/5170566f-a977-4b1f-9083-9de128db20fd" />
<img width="1871" height="806" alt="image" src="https://github.com/user-attachments/assets/bab99dc1-cc52-4d42-babd-2b9166e0262a" />




---

##  Ingestion Pipeline
### 1 Text extraction from PDF using PDFplumber
### 2 Section Based Parsing:

  The system currently extracts only predefined FDA sections:
  
  -  INDICATIONS AND USAGE
  -  DOSAGE AND ADMINISTRATION  
  - DOSAGE FORMS AND STRENGTHS       
  -  CONTRAINDICATIONS   
  - WARNINGS AND PRECAUTIONS
  - ADVERSE REACTIONS 
  - DRUG INTERACTIONS
  - USE IN SPECIFIC POPULATIONS
        
  Only text under these sections are stored, rest is ignored

### 4. Split text into chunks with overlapping
### 5. Generate embeddings for each chunk
### 6. Store in ChromaDB with metadata:

   * drug name
   * section
   * chunk ID

---

## Retrieval Pipeline

1. User submits query
2. Query is embedded using SentenceTransformer
3. Optional filtering:
   * by drug
   * by section
4. ChromaDB retrieves top-k similar chunks
6. Retrieved context is passed to the LLM

---

## Generation

* Uses local LLM via Ollama (`mistral`)
* Prompt includes:
  * retrieved context
  * user query
* Model generates answer grounded in retrieved text

---

## Running the Project

### Option 1 — Docker (recommended)

**Prerequisites:**
- [Docker Desktop](https://docker.com) installed and running
- [Ollama](https://ollama.ai) installed natively with Mistral pulled

```bash
ollama pull mistral
ollama serve
```

Then in a separate terminal from the project root:

```bash
docker-compose up
```

Open `http://localhost:8501` in your browser.

That's it. Both the API and UI start automatically.

To stop:
```bash
docker-compose down
```

---

### Option 2 — Local (manual)

**Prerequisites:**
- Python 3.12
- Ollama installed with Mistral pulled

```bash
# 1. Clone and set up environment
git clone https://github.com/yourusername/rxlens
cd rxlens
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt

# 2. Start Ollama
ollama serve
ollama pull mistral

# 3. Ingest drug label PDFs
# Place PDFs in data/pdfs/ then run:
python src/ingest.py

# 4. Terminal 1 — Start API
cd src
uvicorn api:app --reload

# 5. Terminal 2 — Start UI
cd src
streamlit run ui.py
```

Open `http://localhost:8501` in your browser.

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/query` | Ask a question, returns answer + sources |
| `GET` | `/drugs` | List all indexed drug labels |
| `POST` | `/ingest` | Upload and index a new PDF |

Auto-generated API docs available at `http://localhost:8000/docs`

---



## Current Features

* PDF ingestion and indexing
* Persistent vector database
* Section-aware chunking
* Semantic search using embeddings
* Basic filtering (drug / section)
* Local LLM-based answer generation
* Streamlit UI for interaction
* FastAPI endpoints for ingestion and querying

---

## Limitations
* Only predifned sections are parsed, there is only partial document coverage
* There is no dynamic section detection
* Chunking is only character based, can break mid sentenecs
* There is no query understanding
* Multi- drug queries may not be handled properly
* No caching
* Sensitive to PDF formatting inconsistencies
  
---

### In Progress
- HyDE (Hypothetical Document Embeddings) — generates a hypothetical answer first, embeds that instead of the raw question, significantly improves retrieval accuracy
- Evaluation framework — automated test set to measure retrieval precision
- Hybrid search — combining semantic search with BM25 keyword search for better handling of medical terminology

### Planned
- Cross-encoder reranking for higher retrieval precision
- Conversation history for multi-turn queries
- Dynamic section detection for non-standard label formats
- Authentication and multi-user support

---

## Key Idea

This project demonstrates how to build a structured, domain-specific RAG system that:

* grounds answers in real data
* reduces hallucination
* handles semi-structured documents (PDFs)
* runs fully locally without external APIs

---

## Notes

* Designed as a learning and systems project
* Focuses on retrieval quality and pipeline design over UI complexity
* Built without LangChain for better control and understanding
