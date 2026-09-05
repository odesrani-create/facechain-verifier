import sys

from face.encoder import FaceEncoder


def main():
    if len(sys.argv) != 2:
        print("Usage: python src/test_encoder.py <image>")
        sys.exit(1)

    image_path = sys.argv[1]

    try:
        encoder = FaceEncoder()

        print("Loading face model...")
        result = encoder.encode(image_path)

        embedding = result["embedding"]

        print("\nFace encoding successful!")
        print(f"Detection confidence: {result['det_score']:.4f}")
        print(f"Embedding dimensions: {len(embedding)}")
        print(f"Bounding box: {result['bbox']}")

        print("\nFirst 10 embedding values:")
        print(embedding[:10])

    except Exception as exc:
        print(f"Error: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
