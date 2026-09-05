import numpy as np


class FaceMatcher:
    """
    Compare two normalized face embeddings using
    cosine similarity.
    """

    def __init__(self, threshold: float = 0.45):
        self.threshold = threshold

    def similarity(
        self,
        embedding_a: list[float],
        embedding_b: list[float],
    ) -> float:

        a = np.asarray(
            embedding_a,
            dtype=np.float32,
        )

        b = np.asarray(
            embedding_b,
            dtype=np.float32,
        )

        if a.shape != b.shape:
            raise ValueError(
                "Face embeddings must have "
                "the same dimensions."
            )

        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)

        if norm_a == 0 or norm_b == 0:
            raise ValueError(
                "Face embedding cannot have zero norm."
            )

        a = a / norm_a
        b = b / norm_b

        score = float(
            np.dot(a, b)
        )

        return score

    def is_match(
        self,
        embedding_a: list[float],
        embedding_b: list[float],
    ) -> bool:

        score = self.similarity(
            embedding_a,
            embedding_b,
        )

        return score >= self.threshold
