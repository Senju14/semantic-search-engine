# Semantic Search Engine

A semantic and hybrid search system using vector database (e.g. Pinecone), PostgreSQL, and CLIP model integration.

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
- Pinecone / FAISS
- PostgreSQL
- SentenceTransformers, OpenAI CLIP
- SQLAlchemy, Pydantic
