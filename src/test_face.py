import sys

from face.detector import detect_faces


def main():
    if len(sys.argv) != 2:
        print("Usage: python src/test_face.py <image>")
        sys.exit(1)

    image_path = sys.argv[1]

    try:
        faces = detect_faces(image_path)

        print(f"\nFaces detected: {len(faces)}")

        for index, face in enumerate(faces, start=1):
            print(f"Face {index}: {face}")

    except Exception as exc:
        print(f"Error: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
