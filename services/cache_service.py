from functools import lru_cache

from services.embedding_service import (
    create_embedding
)


@lru_cache(maxsize=1000)
def cached_embedding(query):

    return create_embedding(
        query
    )