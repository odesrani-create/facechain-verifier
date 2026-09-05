import sys

from search.web_search import WebImageSearch


def main():
    if len(sys.argv) != 2:
        print("Usage: python src/test_search.py <image>")
        sys.exit(1)

    image_path = sys.argv[1]

    try:
        print("=" * 50)
        print("GENUINE WEB / VISUAL SEARCH")
        print("=" * 50)

        searcher = WebImageSearch()
        results = searcher.search(image_path)

        matches = results.get("visual_matches", [])

        print(f"\nVisual matches found: {len(matches)}")

        for i, result in enumerate(matches[:5], 1):
            print(f"\n--- Result {i} ---")
            print("Title:", result.get("title"))
            print("URL:", result.get("link"))
            print("Thumbnail:", result.get("thumbnail"))

    except Exception as exc:
        print(f"\nERROR: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
