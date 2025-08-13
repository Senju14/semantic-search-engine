# Semantic Search Engine

A semantic and hybrid search system using vector database (e.g. Pinecone), PostgreSQL, and CLIP model integration.

<img width="10000" height="5000" alt="image" src="https://github.com/user-attachments/assets/29ca7491-ad29-42b9-88af-7cd7dc7fb7d4" />

## Features

- Vector database setup (Pinecone)
- Embedding generation with SentenceTransformers & CLIP
- REST API with FastAPI:
  - Add product data (name, description, etc.)
  - Semantic search via natural language
- Hybrid search (PostgreSQL full-text + vector similarity)
- Auto pipeline for new data → embedding + storage
- Image-text matching via CLIP model

## Tech Stack

- Python, FastAPI
- Pinecone 
- PostgreSQL
- SentenceTransformers, CLIP
