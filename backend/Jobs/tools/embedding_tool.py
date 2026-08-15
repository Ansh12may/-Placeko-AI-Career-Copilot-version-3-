"""
Embedding Tool

Supports two execution modes:

1. Local development:
   BAAI/bge-small-en-v1.5 is loaded locally using
   SentenceTransformer.

2. Production:
   Embedding inference is delegated to a hosted
   inference API so the Render instance does not
   load the ML model into memory.
"""

from typing import List, Optional
import os

import requests
from sentence_transformers import SentenceTransformer


class EmbeddingTool:

    MODEL_NAME = "BAAI/bge-small-en-v1.5"

    def __init__(self):
        self.model: Optional[SentenceTransformer] = None

        self.use_remote = (
            os.getenv(
                "USE_REMOTE_EMBEDDINGS",
                "false",
            ).lower()
            == "true"
        )

        self.hf_token = os.getenv("HF_TOKEN")

    # =========================================================
    # Local Model
    # =========================================================

    def _get_model(self) -> SentenceTransformer:

        if self.model is None:

            self.model = SentenceTransformer(
                self.MODEL_NAME
            )

        return self.model

    # =========================================================
    # Remote Embedding
    # =========================================================

    def _get_remote_embedding(
        self,
        text: str,
    ) -> List[float]:

        if not self.hf_token:
            raise RuntimeError(
                "HF_TOKEN is required when "
                "USE_REMOTE_EMBEDDINGS=true."
            )

        url = (
            "https://router.huggingface.co/"
            "hf-inference/models/"
            f"{self.MODEL_NAME}"
        )

        headers = {
            "Authorization": (
                f"Bearer {self.hf_token}"
            ),
            "Content-Type": "application/json",
        }

        response = requests.post(
            url,
            headers=headers,
            json={
                "inputs": text,
            },
            timeout=60,
        )

        response.raise_for_status()

        embedding = response.json()

        # Some inference responses can return
        # token-level embeddings.
        if (
            isinstance(embedding, list)
            and embedding
            and isinstance(embedding[0], list)
        ):

            vectors = embedding
            dimension = len(vectors[0])

            pooled = [
                sum(token[i] for token in vectors)
                / len(vectors)
                for i in range(dimension)
            ]

            return pooled

        if isinstance(embedding, list):
            return embedding

        raise RuntimeError(
            "Unexpected embedding response from "
            "Hugging Face."
        )

    # =========================================================
    # Single Embedding
    # =========================================================

    def get_embedding(
        self,
        text: str,
    ) -> List[float]:

        if not text or not text.strip():
            return []

        # -----------------------------------------------------
        # Production
        # -----------------------------------------------------

        if self.use_remote:

            return self._get_remote_embedding(
                text
            )

        # -----------------------------------------------------
        # Local development
        # -----------------------------------------------------

        model = self._get_model()

        embedding = model.encode(
            text,
            normalize_embeddings=True,
        )

        return embedding.tolist()

    # =========================================================
    # Multiple Embeddings
    # =========================================================

    def get_embeddings(
        self,
        texts: List[str],
    ) -> List[List[float]]:

        if not texts:
            return []

        # Remove empty inputs while preserving
        # the relationship between valid texts
        # and generated embeddings.

        cleaned_texts = [
            text.strip()
            for text in texts
            if text and text.strip()
        ]

        if not cleaned_texts:
            return []

        # -----------------------------------------------------
        # Local development
        # -----------------------------------------------------

        if not self.use_remote:

            model = self._get_model()

            embeddings = model.encode(
                cleaned_texts,
                normalize_embeddings=True,
            )

            return embeddings.tolist()

        # -----------------------------------------------------
        # Production
        # -----------------------------------------------------
        #
        # Keep remote requests one-by-one for now.
        # We will optimize this after verifying the
        # inference provider's batch response format.
        # -----------------------------------------------------

        return [
            self._get_remote_embedding(text)
            for text in cleaned_texts
        ]