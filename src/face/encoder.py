from pathlib import Path
import logging
import warnings
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO

import cv2
import numpy as np
from insightface.app import FaceAnalysis


logging.getLogger("insightface").setLevel(logging.ERROR)
logging.getLogger("onnxruntime").setLevel(logging.ERROR)

warnings.filterwarnings(
    "ignore",
    category=FutureWarning,
)


class FaceEncoder:

    def __init__(self):

        output = StringIO()

        with redirect_stdout(output), redirect_stderr(output):

            self.app = FaceAnalysis(
                name="buffalo_l",
                providers=[
                    "CPUExecutionProvider"
                ],
            )

            self.app.prepare(
                ctx_id=0,
                det_size=(640, 640),
            )

    def encode(self, image_path: str) -> dict:

        path = Path(image_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Image not found: {path}"
            )

        image = cv2.imread(str(path))

        if image is None:
            raise ValueError(
                f"Could not read image: {path}"
            )

        output = StringIO()

        with redirect_stdout(output), redirect_stderr(output):

            faces = self.app.get(image)

        if not faces:
            raise ValueError(
                "No face detected."
            )

        face = max(
            faces,
            key=lambda f:
            (f.bbox[2] - f.bbox[0])
            *
            (f.bbox[3] - f.bbox[1]),
        )

        embedding = face.embedding.astype(
            np.float32
        )

        embedding = embedding / np.linalg.norm(
            embedding
        )

        return {
            "embedding": embedding.tolist(),
            "bbox": face.bbox.tolist(),
            "det_score": float(
                face.det_score
            ),
        }
