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
        self.model = SentenceTransformer(
            "BAAI/bge-small-en-v1.5"
        )
    def get_embedding(self, text: str) -> List[float]:
        if not text.strip():
            return []
        embedding = self.model.encode(
            text,
            normalize_embeddings=True
        )
        return embedding.tolist()