from pathlib import Path
import requests


class CandidateDownloader:
    """
    Download candidate images returned by Google Lens.
    """

    def __init__(self, output_dir: str = "data/candidates"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    def download(
        self,
        image_url: str,
        index: int,
    ) -> Path:

        if not image_url:
            raise ValueError(
                "Candidate image URL is empty."
            )

        output_path = (
            self.output_dir
            / f"candidate_{index}.jpg"
        )

        response = requests.get(
            image_url,
            timeout=30,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 "
                    "(X11; Linux x86_64) "
                    "AppleWebKit/537.36 "
                    "Chrome/140 Safari/537.36"
                )
            },
        )

        response.raise_for_status()

        content_type = response.headers.get(
            "content-type",
            "",
        )

        if not content_type.startswith("image/"):
            raise ValueError(
                f"URL did not return an image: "
                f"{content_type}"
            )

        output_path.write_bytes(
            response.content
        )

        return output_path
