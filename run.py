#!/usr/bin/env python3

import re
import sys
import time
import subprocess
import threading
import hashlib
import warnings
from contextlib import redirect_stdout, redirect_stderr
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from pathlib import Path
from urllib.parse import quote
from io import StringIO

from face.encoder import FaceEncoder
from search.web_search import GoogleLensSearcher
from verification.verifier import CandidateVerifier
from blockchain.local_chain import LocalBlockchain
from blockchain.fingerprint import create_fingerprint
from cli.ui import (
    banner,
    section,
    success,
    failure,
    info,
    matches_table,
    complete,
)


PROJECT_ROOT = Path(__file__).resolve().parent


class QuietHandler(SimpleHTTPRequestHandler):

    def log_message(self, format, *args):
        pass


def start_image_server(image_path: Path):

    directory = image_path.parent

    class Handler(QuietHandler):

        def __init__(self, *args, **kwargs):
            super().__init__(
                *args,
                directory=str(directory),
                **kwargs,
            )

    server = TCPServer(
        ("127.0.0.1", 0),
        Handler,
    )

    port = server.server_address[1]

    thread = threading.Thread(
        target=server.serve_forever,
        daemon=True,
    )

    thread.start()

    return server, port


def start_cloudflare(port):

    process = subprocess.Popen(
        [
            "cloudflared",
            "tunnel",
            "--url",
            f"http://127.0.0.1:{port}",
            "--no-autoupdate",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    public_url = None
    start_time = time.time()

    while time.time() - start_time < 20:

        line = process.stdout.readline()

        if not line:
            continue

        match = re.search(
            r"https://[a-zA-Z0-9-]+\.trycloudflare\.com",
            line,
        )

        if match:
            public_url = match.group(0)
            break

    if not public_url:

        process.terminate()

        raise RuntimeError(
            "Could not obtain Cloudflare tunnel URL."
        )

    return process, public_url


def quiet_face_encoder():

    warnings.filterwarnings(
        "ignore",
        category=FutureWarning,
        module="insightface",
    )

    buffer_out = StringIO()
    buffer_err = StringIO()

    with redirect_stdout(buffer_out), redirect_stderr(buffer_err):
        encoder = FaceEncoder()

    return encoder


def verify_command(image_path: str):

    path = Path(image_path).expanduser().resolve()

    banner()

    if not path.exists():

        failure(
            "Input image not found",
            str(path),
        )

        return 1

    section("FACE ANALYSIS")

    try:

        encoder = quiet_face_encoder()

        face = encoder.encode(str(path))

        success("Face detected")
        success(
            "Confidence",
            f"{face['det_score'] * 100:.2f}%",
        )
        success(
            "Embedding",
            f"{len(face['embedding'])} dimensions",
        )

    except Exception as error:

        failure(
            "Face processing failed",
            str(error),
        )

        return 1

    server = None
    tunnel = None

    try:

        section("WEB SEARCH")

        info(
            "Provider",
            "Google Lens / SerpApi",
        )

        server, port = start_image_server(path)

        tunnel, public_url = start_cloudflare(port)

        image_url = (
            f"{public_url}/{quote(path.name)}"
        )

        searcher = GoogleLensSearcher()

        results = searcher.search(image_url)

        success(
            "Visual matches",
            len(results),
        )

        if not results:

            failure(
                "No visual matches found"
            )

            return 1

        section("FACE VERIFICATION")

        verifier = CandidateVerifier(
            threshold=0.45
        )

        verified = verifier.verify(
            str(path),
            results[:10],
        )

        matches_table(verified)

        valid_matches = [
            item
            for item in verified
            if item.get("match")
        ]

        if not valid_matches:

            failure(
                "No face-verified social media match found"
            )

            return 1

        best = valid_matches[0]

        console_title = best.get("title") or "Untitled"
        source = best.get("source") or "Unknown"

        section("BEST MATCH")

        success(
            "Source",
            source,
        )

        success(
            "Post",
            console_title[:80],
        )

        success(
            "Similarity",
            f"{best['similarity']:.4f}",
        )

        success(
            "Match",
            "FACE VERIFIED",
        )

        info(
            "URL",
            best.get("url"),
        )

        section("BLOCKCHAIN")

        record = {
            "type": "face_verification",
            "source": best.get("source"),
            "title": best.get("title"),
            "url": best.get("url"),
            "similarity": round(
                best["similarity"],
                6,
            ),
            "face_embedding_dimensions": len(
                face["embedding"]
            ),
        }

        fingerprint = create_fingerprint(record)

        success(
            "SHA-256 fingerprint",
            fingerprint,
        )

        chain = LocalBlockchain()

        block = chain.add_record(
            {
                "type": "face_verification",
                "fingerprint": fingerprint,
                "record": record,
            }
        )

        success(
            "Block created",
            block["index"],
        )

        verification = chain.verify_block(
            block["index"]
        )

        if verification["verified"]:

            success(
                "Blockchain hash",
                "VALID",
            )

            success(
                "Previous hash",
                "VALID",
            )

            success(
                "Re-verification",
                "VALID",
            )

        else:

            failure(
                "Blockchain verification",
                "FAILED",
            )

            return 1

        complete(
            block["index"],
            fingerprint,
        )

        return 0

    except Exception as error:

        failure(
            "Pipeline failed",
            str(error),
        )

        return 1

    finally:

        if server:

            try:
                server.shutdown()
                server.server_close()
            except Exception:
                pass

        if tunnel:

            try:
                tunnel.terminate()
                tunnel.wait(timeout=5)
            except Exception:

                try:
                    tunnel.kill()
                except Exception:
                    pass


def search_command(image_path: str):

    path = Path(image_path).expanduser().resolve()

    if not path.exists():

        print(
            f"ERROR: Image not found: {path}"
        )

        return 1

    encoder = quiet_face_encoder()
    face = encoder.encode(str(path))

    server = None
    tunnel = None

    try:

        server, port = start_image_server(path)

        tunnel, public_url = start_cloudflare(
            port
        )

        image_url = (
            f"{public_url}/{quote(path.name)}"
        )

        searcher = GoogleLensSearcher()

        results = searcher.search(
            image_url
        )

        print()
        print("=" * 60)
        print("GOOGLE LENS RESULTS")
        print("=" * 60)
        print()

        for index, result in enumerate(
            results[:10],
            1,
        ):

            print(
                f"--- MATCH {index} ---"
            )

            print(
                f"Title : {result.get('title')}"
            )

            print(
                f"Source: {result.get('source')}"
            )

            print(
                f"URL   : {result.get('url')}"
            )

            print()

        print(
            f"Total visual matches: {len(results)}"
        )

        return 0

    finally:

        if server:

            server.shutdown()
            server.server_close()

        if tunnel:

            try:
                tunnel.terminate()
                tunnel.wait(timeout=5)
            except Exception:
                pass


def main():

    if len(sys.argv) < 2:

        print()
        print(
            "FaceChain Verifier"
        )
        print()
        print(
            "Usage:"
        )
        print(
            "  facechain verify <image>"
        )
        print(
            "  facechain search <image>"
        )
        print()

        return 1

    command = sys.argv[1]

    if command == "verify":

        if len(sys.argv) != 3:

            print(
                "Usage: facechain verify <image>"
            )

            return 1

        return verify_command(
            sys.argv[2]
        )

    if command == "search":

        if len(sys.argv) != 3:

            print(
                "Usage: facechain search <image>"
            )

            return 1

        return search_command(
            sys.argv[2]
        )

    print(
        f"Unknown command: {command}"
    )

    print()

    print(
        "Available commands:"
    )

    print(
        "  facechain verify <image>"
    )

    print(
        "  facechain search <image>"
    )

    return 1


if __name__ == "__main__":
    sys.exit(main())
