## Project Workflow

## Step-1. Convert Videos to Audio

Video files are converted into MP3 audio files using FFmpeg.

# --> python videos_to_mp3.py


## Step-2. Generate Transcripts + Semantic Chunks

Audio files are transcribed using Faster Whisper and divided into semantic chunks.
# --> python preprocessing_json.py

This creates transcript JSON files inside:

jsons/
## Step-3. Generate Embeddings

Embeddings are created using Ollama's nomic-embed-text model.

# -->python read_chunks.py

This generates:

embeddings.parquet
## Step-4. Generate YouTube Metadata

Automatically extracts:

YouTube IDs
Titles
URLs

from the Sigma course playlist using yt-dlp.

# --> python generate_video_data.py

This creates:
    video_data.py

## Step-5. Run AI Search Engine

Launch the Flask application:

# -->python app.py

Open:

http://127.0.0.1:5000

## PROJECT STRUCTURE
project/
│
├── __pycache__/
├── .vscode/
├── audios/
├── jsons/
├── static/
│   ├── script.js
│   └── style.css
│
├── templates/
│   └── index.html
│
├── venv/
├── videos/
│
├── .gitignore
├── app.py
├── embeddings.parquet
├── generate_video_data.py
├── main.py
├── preprocessing_json.py
├── process_incoming.py
├── prompt.txt
├── read_chunks.py
├── README.md
├── requirements.txt
├── response.txt
├── video_data.py
├── videos_to_mp3.py