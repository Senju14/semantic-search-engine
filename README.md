# Semantic Search Engine

A semantic and hybrid search system using vector database (e.g. Pinecone), PostgreSQL, and CLIP model integration.

<img width="3000" height="1500" alt="image" src="https://github.com/user-attachments/assets/c5b73857-82aa-4bac-beca-083bc9827ce6" />

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
