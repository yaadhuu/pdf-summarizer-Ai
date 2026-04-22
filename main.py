from fastapi import FastAPI, HTTPException, UploadFile, File
from pdf_parser import extract_text_from_pdf
from chunker import split_text_into_chunks
from embedder import store_chunks, query_chunks
from chat import get_answer
import shutil
import os
import uuid

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (for local testing)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

collections = {}

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    
    unique_id = uuid.uuid4().hex
    temp_path = f"temp_{unique_id}.pdf"
    
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    text = extract_text_from_pdf(temp_path)
    os.remove(temp_path)
    
    chunks = split_text_into_chunks(text)
    if not chunks:
        raise HTTPException(status_code=400, detail="Could not extract any text from the PDF. It might be scanned or empty.")
    
    collection_name = f"doc_{unique_id}"
    client, collection = store_chunks(chunks, collection_name)
   
    collections[collection_name] = collection

    return {
        "filename": file.filename,
        "total_chunks": len(chunks),
        "collection_name": collection_name,
        "message": "PDF uploaded successfully!"
    }

@app.post("/ask/")
async def ask_question(collection_name: str, mode: str = "chat", question: str = ""):
    
 
    if collection_name not in collections:
        raise HTTPException(status_code=404, detail="PDF not found. Upload it first.")
    
  
    collection = collections[collection_name]
    
    if mode == "summary":
        # Get all chunks instead of searching for relevance
        results = collection.get()
        relevant_chunks = results["documents"]
        # Limit to 100 chunks roughly matching Groq's maximum free tier request limits for context
        relevant_chunks = relevant_chunks[:100] 
    else:
        if not question:
            raise HTTPException(status_code=400, detail="Question is required for this mode.")
        relevant_chunks = query_chunks(collection, question)
    
 
    answer = get_answer(question, relevant_chunks, mode)
    
    return {
        "question": question,
        "mode": mode,
        "answer": answer
    }