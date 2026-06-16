import numpy as np
import faiss

from config import TOP_RESULTS


def retrieve_chunks(
    question_embedding,
    index,
    df
):

    query = np.array(
        [question_embedding],
        dtype="float32"
    )
    faiss.normalize_L2(
        query
    )

    scores, indices = index.search(
        query,
        TOP_RESULTS
    )

    max_indx = indices[0]

    similarities = scores[0]

    new_df = df.iloc[max_indx]

    return (
        new_df,
        similarities,
        max_indx
    )