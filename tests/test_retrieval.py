import numpy as np
import pandas as pd
import faiss

from services.retrieval_service import (
    retrieve_chunks
)


def test_retrieve_chunks():

    embeddings = np.array([
        [1.0, 0.0],
        [0.0, 1.0],
        [0.9, 0.1]
    ], dtype="float32")

    faiss.normalize_L2(
        embeddings
    )

    index = faiss.IndexFlatIP(2)

    index.add(
        embeddings
    )

    df = pd.DataFrame({
        "text": [
            "python",
            "javascript",
            "python tutorial"
        ]
    })

    query = np.array(
        [1.0, 0.0],
        dtype="float32"
    )

    new_df, similarities, max_indx = (
        retrieve_chunks(
            query,
            index,
            df
        )
    )

    assert len(new_df) > 0

    assert (
        new_df.iloc[0]["text"]
        == "python"
    )