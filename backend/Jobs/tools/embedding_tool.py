"""
Embedding Tool
Responsible for generating vector embeddings
using the configured embedding model.
This tool performs NO ranking or AI reasoning.

Responsibilities:
- Generate embedding vector
- Return embedding vector
"""

from typing import List
from sentence_transformers import SentenceTransformer


class EmbeddingTool:

    def __init__(self):
        # Do NOT load the model during application startup.
        self.model = None

    def _get_model(self):
        """
        Lazily load the embedding model only when
        an embedding is actually required.
        """
        if self.model is None:
            self.model = SentenceTransformer(
                "BAAI/bge-small-en-v1.5"
            )

        return self.model

    def get_embedding(self, text: str) -> List[float]:

        if not text.strip():
            return []

        model = self._get_model()

        embedding = model.encode(
            text,
            normalize_embeddings=True
        )

        return embedding.tolist()