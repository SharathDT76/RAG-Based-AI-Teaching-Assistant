import requests
import os
import json
import pandas as pd
import time

# -----------------------------------
# Create Embeddings Function
# -----------------------------------
def create_embedding(text_list):

    r = requests.post(
        "http://localhost:11434/api/embed",
        json={
            "model": "nomic-embed-text",
            "input": text_list
        }
    )

    r.raise_for_status()

    data = r.json()

    return data["embeddings"]


# -----------------------------------
# Read JSON Files
# -----------------------------------
jsons = [
    f for f in os.listdir("jsons")
    if f.endswith(".json")
]

my_dicts = []
chunk_id = 0

# Batch size for embeddings
BATCH_SIZE = 64

# -----------------------------------
# Process Each JSON
# -----------------------------------
for json_file in jsons:

    with open(f"jsons/{json_file}", encoding="utf-8") as f:
        content = json.load(f)

    print(f"\nCreating Embeddings for {json_file}")

    chunks = content["chunks"]

    # -----------------------------------
    # Batch Processing
    # -----------------------------------
    for start in range(0, len(chunks), BATCH_SIZE):

        batch_chunks = chunks[start:start + BATCH_SIZE]

        texts = [
            c["text"]
            for c in batch_chunks
        ]

        embeddings = create_embedding(texts)

        # -----------------------------------
        # Store Embeddings
        # -----------------------------------
        for i, chunk in enumerate(batch_chunks):

            chunk["chunk_id"] = chunk_id
            chunk["source_file"] = json_file
            chunk["embedding"] = embeddings[i]

            my_dicts.append(chunk)

            chunk_id += 1

        print(
            f"Processed chunks "
            f"{start} -> "
            f"{start + len(batch_chunks)}"
        )

        # Small delay prevents overload
        time.sleep(0.3)

# -----------------------------------
# Create DataFrame
# -----------------------------------
df = pd.DataFrame.from_records(my_dicts)

# Optional cleanup
if "number" in df.columns:
    df["number"] = df["number"].astype(int)

# -----------------------------------
# Save Data
# -----------------------------------
df.to_parquet("embeddings.parquet", index=False)

# Optional CSV
# df.to_csv("embeddings.csv", index=False)

# -----------------------------------
# Output
# -----------------------------------
print("\n===================================")
print("Embeddings Created Successfully")
print("===================================")

print(f"Total Chunks: {len(df)}")

print("\nDataFrame Preview:\n")
print(df.head())