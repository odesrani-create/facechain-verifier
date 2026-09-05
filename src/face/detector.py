from pathlib import Path

import cv2


CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"


def detect_faces(image_path: str) -> list[dict]:
    """Detect faces in an image and return bounding boxes."""
    path = Path(image_path)

    if not path.exists():
        raise FileNotFoundError(f"Image not found: {path}")

    image = cv2.imread(str(path))

    if image is None:
        raise ValueError(f"Could not read image: {path}")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    detector = cv2.CascadeClassifier(CASCADE_PATH)

    if detector.empty():
        raise RuntimeError("Failed to load OpenCV Haar cascade.")

    faces = detector.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(60, 60),
    )

    results = []

    for x, y, width, height in faces:
        results.append(
            {
                "x": int(x),
                "y": int(y),
                "width": int(width),
                "height": int(height),
            }
        )

    return results
