#!/usr/bin/env python3
"""
AI Conversation Archive Search - Embedding & Index Script
Converts conversation exports into searchable semantic memory
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Tuple

# Check dependencies
try:
    from sentence_transformers import SentenceTransformer
    import chromadb
    from chromadb.config import Settings
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("\nInstall with:")
    print("  pip install sentence-transformers chromadb")
    sys.exit(1)

# Configuration - EDIT THESE PATHS
VAULT_PATH = Path(r"./conversation_exports")  # Point to your markdown files
DB_PATH = Path(r"./chroma_db")  # Vector database location
COLLECTION_NAME = "conversation_chunks"
MODEL_NAME = "all-MiniLM-L6-v2"  # Small, fast, good quality
CHUNK_SIZE = 2000  # characters per chunk
CHUNK_OVERLAP = 200  # overlap between chunks


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    """Split text into overlapping chunks for better context preservation."""
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
        
        if end >= len(text):
            break
    
    return chunks


def find_markdown_files(root_path: Path) -> List[Path]:
    """Recursively find all markdown files."""
    md_files = []
    for file in root_path.rglob("*.md"):
        if file.is_file():
            md_files.append(file)
    return md_files


def index_conversations(model, collection, vault_path: Path, incremental: bool = False):
    """Index all conversation files into ChromaDB."""
    print(f"Scanning for markdown files in: {vault_path}")
    md_files = find_markdown_files(vault_path)
    
    if not md_files:
        print(f"No markdown files found in {vault_path}")
        print("Check your VAULT_PATH configuration")
        return
    
    print(f"Found {len(md_files)} files")
    
    # Get already indexed files if incremental
    indexed_files = set()
    if incremental:
        try:
            existing = collection.get(include=["metadatas"])
            indexed_files = {m["source_file"] for m in existing["metadatas"] if "source_file" in m}
            print(f"Skipping {len(indexed_files)} already indexed files")
        except:
            pass
    
    total_chunks = 0
    processed = 0
    
    for md_file in md_files:
        relative_path = str(md_file.relative_to(vault_path))
        
        if incremental and relative_path in indexed_files:
            continue
        
        try:
            # Read file
            with open(md_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            if not content.strip():
                continue
            
            # Chunk the text
            chunks = chunk_text(content)
            
            if not chunks:
                continue
            
            # Generate embeddings
            embeddings = model.encode(chunks)
            
            # Create IDs and metadata
            file_id = md_file.stem
            ids = [f"{file_id}_{i}" for i in range(len(chunks))]
            metadatas = [
                {
                    "source_file": relative_path,
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                    "indexed_at": datetime.now().isoformat()
                }
                for i in range(len(chunks))
            ]
            
            # Add to collection
            collection.add(
                ids=ids,
                embeddings=embeddings.tolist(),
                documents=chunks,
                metadatas=metadatas
            )
            
            total_chunks += len(chunks)
            processed += 1
            
            if processed % 10 == 0:
                print(f"Processed: {processed}/{len(md_files)} files ({total_chunks} chunks)")
        
        except Exception as e:
            print(f"Error processing {md_file.name}: {e}")
            continue
    
    print(f"\nIndexing complete!")
    print(f"Files processed: {processed}")
    print(f"Total chunks indexed: {total_chunks}")


def search_conversations(model, collection, query: str, n_results: int = 5) -> List[Tuple[str, str, float]]:
    """Search the indexed conversations."""
    print(f"\nSearching for: '{query}'")
    print(f"Generating embedding...")
    
    # Generate query embedding
    query_embedding = model.encode([query])[0]
    
    # Search
    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=n_results,
        include=["documents", "metadatas", "distances"]
    )
    
    # Format results
    formatted_results = []
    for i, (doc, metadata, distance) in enumerate(zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    )):
        # Convert distance to similarity score (lower distance = higher similarity)
        similarity = 1 - (distance / 2)  # Normalize to 0-1 range
        
        source_file = metadata.get("source_file", "unknown")
        chunk_index = metadata.get("chunk_index", 0)
        
        formatted_results.append((source_file, doc, similarity))
    
    return formatted_results


def get_stats(collection):
    """Get index statistics."""
    try:
        count = collection.count()
        print(f"\nIndex Statistics:")
        print(f"Total chunks indexed: {count:,}")
        
        # Get sample to show file count estimate
        sample = collection.get(limit=100, include=["metadatas"])
        if sample and sample["metadatas"]:
            unique_files = len(set(m.get("source_file", "") for m in sample["metadatas"]))
            estimated_files = int(unique_files * (count / len(sample["metadatas"])))
            print(f"Estimated files: ~{estimated_files}")
        
        return True
    except Exception as e:
        print(f"Error getting stats: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="AI Conversation Archive Search")
    parser.add_argument("--index", action="store_true", help="Index conversations")
    parser.add_argument("--incremental", action="store_true", help="Only index new files")
    parser.add_argument("--search", type=str, help="Search query")
    parser.add_argument("--n_results", type=int, default=5, help="Number of results")
    parser.add_argument("--stats", action="store_true", help="Show index statistics")
    
    args = parser.parse_args()
    
    if not any([args.index, args.search, args.stats]):
        parser.print_help()
        return
    
    # Verify paths
    if not VAULT_PATH.exists():
        print(f"Error: VAULT_PATH does not exist: {VAULT_PATH}")
        print("Edit VAULT_PATH in this script to point to your conversation exports")
        return
    
    # Initialize
    print("Loading embedding model...")
    model = SentenceTransformer(MODEL_NAME)
    
    print("Connecting to database...")
    DB_PATH.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(DB_PATH))
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"description": "AI conversation archive embeddings"}
    )
    
    # Execute commands
    if args.stats:
        get_stats(collection)
    
    if args.index:
        print("\nStarting indexing...")
        index_conversations(model, collection, VAULT_PATH, incremental=args.incremental)
    
    if args.search:
        results = search_conversations(model, collection, args.search, args.n_results)
        
        print(f"\nFound {len(results)} results:\n")
        for i, (source, text, similarity) in enumerate(results, 1):
            print(f"{'='*80}")
            print(f"Result {i} | Relevance: {similarity:.3f}")
            print(f"Source: {source}")
            print(f"\n{text}\n")
        print(f"{'='*80}")


if __name__ == "__main__":
    main()
