# RAG-Based AI Assistant

A Retrieval-Augmented Generation (RAG) application that allows users to semantically search Sigma Web Development Course videos and instantly jump to the most relevant timestamp.

The application uses Ollama embeddings, FAISS vector search, Flask, and YouTube timestamp linking to provide fast and accurate video retrieval.

---

## Features

* Semantic video search using vector embeddings
* FAISS-based similarity search
* Ollama `nomic-embed-text` embeddings
* YouTube timestamp navigation
* Flask web interface
* Rate limiting and input validation
* Docker support
* Automated tests with Pytest
* Modular service-based architecture

---

## Tech Stack

### Backend

* Flask
* Python

### Vector Search

* FAISS
* NumPy
* Pandas

### Embeddings

* Ollama
* nomic-embed-text

### Testing

* Pytest

### Deployment

* Docker
* Gunicorn

---

## Data Processing Pipeline

### Step 1: Convert Videos to Audio

Convert video files into MP3 format using FFmpeg.

```bash
python scripts/videos_to_mp3.py
```

---

### Step 2: Generate Transcripts and Semantic Chunks

Transcribe audio files using Faster Whisper and split transcripts into semantic chunks.

```bash
python scripts/preprocessing_json.py
```

Generated output:

```text
data/jsons/
```

---

### Step 3: Create Embeddings

Generate embeddings using Ollama's `nomic-embed-text` model.

```bash
python scripts/read_chunks.py
```

Generated output:

```text
data/embeddings.parquet
```

---

### Step 4: Build FAISS Index

Create the vector index used for semantic search.

```bash
python scripts/build_faiss_index.py
```

Generated output:

```text
data/faiss.index
```

---

### Step 5: Generate Video Metadata

Extract YouTube metadata and build the video mapping.

```bash
python scripts/generate_video_data.py
```

Generated output:

```text
data/video_data.py
```

---

### Step 6: Run the Application

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

## Docker

Build image:

```bash
docker build -t sigma-rag .
```

Run container:

```bash
docker run -p 8000:8000 sigma-rag
```

Open:

```text
http://localhost:8000
```

---

## Running Tests

```bash
pytest
```

---

## Project Structure

```text
RAG-Based AI Assistant
│
├── app.py
├── config.py
├── requirements.txt
├── Dockerfile
├── .gitignore
│
├── data/
│   ├── __init__.py
│   ├── video_data.py
│   ├── embeddings.parquet
│   ├── faiss.index
│   └── jsons/
│
├── services/
│   ├── __init__.py
│   ├── embedding_service.py
│   └── retrieval_service.py
│
├── scripts/
│   ├── build_faiss_index.py
│   ├── generate_video_data.py
│   ├── preprocessing_json.py
│   ├── process_incoming.py
│   ├── read_chunks.py
│   └── videos_to_mp3.py
│
├── tests/
│   ├── __init__.py
│   ├── test_health.py
│   └── test_retrieval.py
│
├── static/
│   ├── script.js
│   └── style.css
│
└── templates/
    └── index.html
```

---

## Search Flow

```text
User Query
     │
     ▼
Ollama Embedding
     │
     ▼
FAISS Search
     │
     ▼
Top Relevant Chunks
     │
     ▼
YouTube Timestamp Links
     │
     ▼
Results Displayed
```
