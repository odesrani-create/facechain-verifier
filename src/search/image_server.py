from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from pathlib import Path
import sys


def main():
    if len(sys.argv) != 2:
        print("Usage: python image_server.py <image>")
        sys.exit(1)

    image_path = Path(sys.argv[1]).resolve()

    if not image_path.exists():
        print(f"Image not found: {image_path}")
        sys.exit(1)

    directory = image_path.parent
    filename = image_path.name

    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(
                *args,
                directory=str(directory),
                **kwargs
            )

    with TCPServer(("127.0.0.1", 8000), Handler) as server:
        print("=" * 50)
        print("LOCAL IMAGE SERVER")
        print("=" * 50)
        print(f"Serving: {image_path}")
        print(f"Local URL: http://127.0.0.1:8000/{filename}")
        print()
        print("Keep this terminal running.")
        print("Press CTRL+C to stop.")
        print("=" * 50)

        server.serve_forever()


if __name__ == "__main__":
    main()
