import requests
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


# ===================================
# Create Embedding Function
# ===================================
def create_embedding(text):

    r = requests.post(
        "http://localhost:11434/api/embed",
        json={
            "model": "nomic-embed-text",
            "input": text
        }
    )

    r.raise_for_status()

    data = r.json()

    return data["embeddings"][0]


# ===================================
# LLM Inference Function
# ===================================
def inference(prompt):

    r = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "llama3.1",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False
        }
    )

    r.raise_for_status()

    response = r.json()

    return response["message"]["content"]


# ===================================
# Load Embeddings
# ===================================
df = pd.read_parquet("embeddings.parquet")

print("Embeddings Loaded")
print(f"Total Chunks: {len(df)}")


# ===================================
# User Query
# ===================================
incoming_query = input("\nAsk a Question: ")


# ===================================
# Create Query Embedding
# ===================================
question_embedding = create_embedding(
    incoming_query
)


# ===================================
# Convert Embeddings To Matrix
# ===================================
embedding_matrix = np.vstack(
    df["embedding"].values
)


# ===================================
# Similarity Search
# ===================================
similarities = cosine_similarity(
    embedding_matrix,
    [question_embedding]
).flatten()


# ===================================
# Get Top Results
# ===================================
top_results = 5

max_indx = similarities.argsort()[::-1][
    :top_results
]

new_df = df.iloc[max_indx]


# ===================================
# Build Context
# ===================================
context = ""

for _, row in new_df.iterrows():

    similarity_score = similarities[
        max_indx[
            new_df.index.get_loc(_)
        ]
    ]

    # Skip weak matches
    if similarity_score < 0.55:
        continue

    context += f"""
Video Title: {row['title']}

Video Number: {row['number']}

Timestamp:
{row['start']}s → {row['end']}s

Transcript:
{row['text']}

----------------------------------------
"""


# ===================================
# Build Prompt
# ===================================
prompt = f"""
You are an assistant for the Sigma Web Development Course.

You help students find exactly where a topic is taught in the course videos.

Below are the most relevant transcript chunks retrieved from the course.

{context}

User Question:
{incoming_query}

Instructions:
- Answer naturally and conversationally.
- Mention:
    - video title
    - video number
    - timestamps
    - what is covered there
- Guide the student to the best video.
- If multiple videos are useful, explain what each one covers.
- Do NOT mention embeddings, chunks, JSON, similarity search, retrieval, or vector database.
- If the question is unrelated to the course, reply:
  "I can only answer questions related to the Sigma Web Development course."
"""


# ===================================
# Save Prompt
# ===================================
with open(
    "prompt.txt",
    "w",
    encoding="utf-8"
) as f:

    f.write(prompt)

print("\nPrompt saved to prompt.txt")


# ===================================
# Run LLM
# ===================================
response = inference(prompt)

print("\n===================================")
print("AI RESPONSE")
print("===================================\n")

print(response)


# ===================================
# Save Response
# ===================================
with open(
    "response.txt",
    "w",
    encoding="utf-8"
) as f:

    f.write(response)

print("\nResponse saved to response.txt")


# ===================================
# Optional Debug Retrieval Display
# ===================================
print("\n===================================")
print("Retrieved Chunks")
print("===================================\n")

for rank, (index, item) in enumerate(
    new_df.iterrows(),
    start=1
):

    similarity_score = similarities[
        max_indx[rank - 1]
    ]

    print(f"Result {rank}")
    print(
        f"Similarity Score : "
        f"{similarity_score:.4f}"
    )

    print(
        f"Video Number    : "
        f"{item['number']}"
    )

    print(
        f"Title           : "
        f"{item['title']}"
    )

    print(
        f"Timestamp       : "
        f"{item['start']}s "
        f"→ "
        f"{item['end']}s"
    )

    print("\nText:\n")

    print(item["text"])

    print("\n" + "=" * 60 + "\n")