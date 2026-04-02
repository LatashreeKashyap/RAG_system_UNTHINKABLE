import sys
import os
from fastapi import FastAPI
from fastapi.responses import RedirectResponse  # <--- Added this

# Helps Python find rag_engine.py inside the app folder
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from rag_engine import get_qa_chain

app = FastAPI()
qa_system = None

# NEW: This makes the main link (http://127.0.0.1:8000) redirect to /docs automatically
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

@app.on_event("startup")
def startup_event():
    global qa_system
    # This might take a moment to load the local AI models
    qa_system = get_qa_chain()

@app.get("/ask")
def ask(query: str):
    if qa_system is None:
        return {"error": "Knowledge base not initialized."}
    
    result = qa_system.invoke(query)
    
    # Extract unique filenames from the retrieved context
    sources = list(set([doc.metadata.get("source", "Unknown") for doc in result["context"]]))
    # Clean up the file path to just show the name
    sources = [os.path.basename(s) for s in sources]
    
    return {
        "answer": result["answer"],
        "sources": sources
    }