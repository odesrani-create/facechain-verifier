from pathlib import Path

from face.encoder import FaceEncoder
from verification.matcher import FaceMatcher
from verification.candidate import CandidateDownloader


class CandidateVerifier:

    def __init__(
        self,
        threshold: float = 0.45,
    ):
        self.encoder = FaceEncoder()
        self.matcher = FaceMatcher(
            threshold=threshold
        )
        self.downloader = CandidateDownloader()

    def verify(
        self,
        original_image: str,
        results: list[dict],
    ) -> list[dict]:

        original_face = self.encoder.encode(
            original_image
        )

        verified = []

        for index, result in enumerate(
            results,
            1,
        ):

            thumbnail = result.get(
                "thumbnail"
            )

            if not thumbnail:
                continue

            try:

                candidate_path = (
                    self.downloader.download(
                        thumbnail,
                        index,
                    )
                )

                candidate_face = (
                    self.encoder.encode(
                        str(candidate_path)
                    )
                )

                score = self.matcher.similarity(
                    original_face["embedding"],
                    candidate_face["embedding"],
                )

                verified.append({
                    "rank": index,
                    "title": result.get(
                        "title"
                    ),
                    "source": result.get(
                        "source"
                    ),
                    "url": result.get(
                        "url"
                    ),
                    "thumbnail": thumbnail,
                    "candidate_image": str(
                        candidate_path
                    ),
                    "similarity": score,
                    "match": (
                        score
                        >= self.matcher.threshold
                    ),
                })

            except Exception as error:

                verified.append({
                    "rank": index,
                    "title": result.get(
                        "title"
                    ),
                    "source": result.get(
                        "source"
                    ),
                    "url": result.get(
                        "url"
                    ),
                    "thumbnail": thumbnail,
                    "candidate_image": None,
                    "similarity": None,
                    "match": False,
                    "error": str(error),
                })

        verified.sort(
            key=lambda item: (
                item["similarity"]
                if item["similarity"] is not None
                else -1
            ),
            reverse=True,
        )

        return verified
