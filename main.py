import requests

r = requests.post("http://localhost:11434/api/embeddings", json={
    "model": "bge-m3",  
    "input": "hello golgappa"
})
embeddings = r.json()["embeddings"]
print(embeddings)
