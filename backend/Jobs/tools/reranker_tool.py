"""
Cross Encoder Reranker Tool

Responsible for computing semantic relevance scores
between a candidate resume and job descriptions.

The CrossEncoder model is loaded lazily so that
application startup does not load the ML model.
"""

from typing import List, Optional

from sentence_transformers import CrossEncoder


class RerankerTool:

    def __init__(self):
        self.model: Optional[CrossEncoder] = None

    def _get_model(self) -> CrossEncoder:

        if self.model is None:
            self.model = CrossEncoder(
                "cross-encoder/ms-marco-MiniLM-L-6-v2"
            )

        return self.model

    def score(
        self,
        resume_text: str,
        job_text: str,
    ) -> float:

        if (
            not resume_text.strip()
            or not job_text.strip()
        ):
            return 0.0

        model = self._get_model()

        score = model.predict(
            [(resume_text, job_text)]
        )

        return float(score[0])

    def score_batch(
        self,
        resume_text: str,
        job_texts: List[str],
    ) -> List[float]:

        if not resume_text.strip():
            return [0.0] * len(job_texts)

        if not job_texts:
            return []

        pairs = [
            (resume_text, job_text)
            for job_text in job_texts
        ]

        model = self._get_model()

        scores = model.predict(pairs)

        return [
            float(score)
            for score in scores
        ]