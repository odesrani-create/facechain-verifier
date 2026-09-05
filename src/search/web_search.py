import requests

from config.settings import (
    SEARCH_PROVIDER,
    SERPAPI_API_KEY,
)


class GoogleLensSearcher:
    """
    Google Lens search through the configured search provider.
    """

    def __init__(self):
        if SEARCH_PROVIDER != "serpapi":
            raise RuntimeError(
                f"Unsupported search provider: {SEARCH_PROVIDER}"
            )

        if not SERPAPI_API_KEY:
            raise RuntimeError(
                "SERPAPI_API_KEY is missing. "
                "Add it to .env"
            )

        self.api_key = SERPAPI_API_KEY

    def search(self, image_url: str) -> list[dict]:
        response = requests.get(
            "https://serpapi.com/search",
            params={
                "engine": "google_lens",
                "url": image_url,
                "api_key": self.api_key,
            },
            timeout=60,
        )

        response.raise_for_status()

        data = response.json()

        matches = data.get(
            "visual_matches",
            []
        )

        results = []

        for match in matches:
            results.append({
                "title": match.get("title"),
                "url": match.get("link"),
                "source": match.get("source"),
                "thumbnail": match.get("thumbnail"),
            })

        return results
