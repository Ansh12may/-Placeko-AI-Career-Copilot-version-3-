"""
Embedding Tool

Responsible for generating vector embeddings.
The model is loaded lazily so application startup
does not download/load the ML model.
"""

from typing import List, Optional

from sentence_transformers import SentenceTransformer


class EmbeddingTool:

    def __init__(self):
        self.model: Optional[SentenceTransformer] = None

    def _get_model(self) -> SentenceTransformer:
        if self.model is None:
            self.model = SentenceTransformer(
                "BAAI/bge-small-en-v1.5"
            )

        return self.model

    def get_embedding(
        self,
        text: str,
    ) -> List[float]:

        if not text.strip():
            return []

        model = self._get_model()

        embedding = model.encode(
            text,
            normalize_embeddings=True,
        )

        return embedding.tolist()