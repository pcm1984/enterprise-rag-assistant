# Enterprise Architecture Knowledge Assistant

A learning-focused implementation of an enterprise RAG system for
answering architecture and engineering questions from internal
documentation.

## Current Architecture

Knowledge Documents
        ↓
Document Ingestion
        ↓
Chunking
        ↓
Embeddings
        ↓
Vector Retrieval
        ↓
LLM

## Current Stack

- Python
- Ollama
- nomic-embed-text
- Markdown knowledge documents

## Current Progress

- [x] Local Python environment
- [x] Local LLM with Ollama
- [x] Document ingestion
- [x] Document chunking
- [x] Contextual chunk representation
- [x] Local embeddings
- [ ] Vector database
- [ ] Semantic retrieval
- [ ] RAG generation
- [ ] Source citations
- [ ] Evaluation
- [ ] Enterprise security considerations
