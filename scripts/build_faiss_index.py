import faiss
import numpy as np
import pandas as pd

df = pd.read_parquet(
    "data/embeddings.parquet"
)

embeddings = np.vstack(
    df["embedding"].values
).astype("float32")

index = faiss.IndexFlatIP(
    embeddings.shape[1]
)

faiss.normalize_L2(
    embeddings
)

index.add(
    embeddings
)

faiss.write_index(
    index,
    "data/faiss.index"
)

print(
    f"Indexed {len(df)} chunks"
)