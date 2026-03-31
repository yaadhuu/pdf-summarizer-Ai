import chromadb
from chromadb.utils import embedding_functions

def store_chunks(chunks: list, collection_name: str):
    
   
    client = chromadb.Client()
    
    
    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
 
    existing = [c.name for c in client.list_collections()]
    if collection_name in existing:
        client.delete_collection(collection_name)
  
    collection = client.create_collection(
        name=collection_name,
        embedding_function=embedding_fn
    )
    
   
    ids = [str(i) for i in range(len(chunks))]
    
  
    collection.add(documents=chunks, ids=ids)
    
    return client, collection

def query_chunks(collection, question: str, n_results: int = 3):
    
    
    results = collection.query(
        query_texts=[question],
        n_results=n_results
    )
    
  
    return results["documents"][0]