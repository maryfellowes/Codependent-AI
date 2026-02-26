#!/usr/bin/env python3
"""
AI Conversation Archive Search Daemon
HTTP server for semantic search queries
Keeps embedding model loaded for fast searches
"""

import os
import sys
from pathlib import Path
from typing import Optional

try:
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel
    from sentence_transformers import SentenceTransformer
    import chromadb
    import uvicorn
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("\nInstall with:")
    print("  pip install fastapi uvicorn sentence-transformers chromadb")
    sys.exit(1)

# Configuration - MUST MATCH embed_vault.py
DB_PATH = Path(r"./chroma_db")
COLLECTION_NAME = "conversation_chunks"
MODEL_NAME = "all-MiniLM-L6-v2"
PORT = 8766

# Global state
model = None
collection = None

# API Models
class SearchRequest(BaseModel):
    query: str
    n_results: int = 5

class SearchResult(BaseModel):
    source_file: str
    text: str
    relevance: float
    chunk_index: int

class SearchResponse(BaseModel):
    query: str
    results: list[SearchResult]
    total: int

class StatsResponse(BaseModel):
    total_chunks: int
    status: str

# FastAPI app
app = FastAPI(title="Conversation Archive Search")


@app.on_event("startup")
async def startup():
    """Load model and connect to database on startup."""
    global model, collection
    
    print("Loading embedding model...")
    model = SentenceTransformer(MODEL_NAME)
    print(f"Model loaded: {MODEL_NAME}")
    
    print("Connecting to ChromaDB...")
    if not DB_PATH.exists():
        print(f"Warning: Database not found at {DB_PATH}")
        print("Run embed_vault.py --index first")
    else:
        client = chromadb.PersistentClient(path=str(DB_PATH))
        collection = client.get_or_create_collection(name=COLLECTION_NAME)
        print(f"Connected to collection: {COLLECTION_NAME}")
    
    print(f"\nSearch daemon ready on http://localhost:{PORT}")


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "collection_connected": collection is not None
    }


@app.get("/stats", response_model=StatsResponse)
async def get_stats():
    """Get index statistics."""
    if collection is None:
        raise HTTPException(status_code=503, detail="Collection not initialized")
    
    try:
        count = collection.count()
        return StatsResponse(
            total_chunks=count,
            status="indexed"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    """Semantic search across conversation archive."""
    if model is None or collection is None:
        raise HTTPException(status_code=503, detail="Service not initialized")
    
    try:
        # Generate query embedding
        query_embedding = model.encode([request.query])[0]
        
        # Search
        results = collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=request.n_results,
            include=["documents", "metadatas", "distances"]
        )
        
        # Format results
        formatted_results = []
        for doc, metadata, distance in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0]
        ):
            # Convert distance to similarity (0-1, higher is better)
            similarity = 1 - (distance / 2)
            
            formatted_results.append(SearchResult(
                source_file=metadata.get("source_file", "unknown"),
                text=doc,
                relevance=similarity,
                chunk_index=metadata.get("chunk_index", 0)
            ))
        
        return SearchResponse(
            query=request.query,
            results=formatted_results,
            total=len(formatted_results)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def main():
    """Run the search daemon."""
    print(f"\nStarting Conversation Archive Search Daemon")
    print(f"Model: {MODEL_NAME}")
    print(f"Database: {DB_PATH}")
    print(f"Port: {PORT}")
    print("-" * 50)
    
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=PORT,
        log_level="info"
    )


if __name__ == "__main__":
    main()
