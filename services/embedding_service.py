import requests
from config import OLLAMA_URL


def create_embedding(text):

    print("=" * 50)
    print("Calling Ollama")
    print(text)

    r = requests.post(
        f"{OLLAMA_URL}/api/embed",
        json={
            "model": "nomic-embed-text",
            "input": text
        },
        timeout=60
    )

    print("Status:", r.status_code)

    r.raise_for_status()

    data = r.json()

    print("Embedding received")

    return data["embeddings"][0]