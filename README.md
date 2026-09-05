# FaceChain Verifier

FaceChain Verifier is a command-line proof of concept that combines face
embedding, reverse-image search, similarity checking, and a local blockchain
record.

> **Important:** This project is for authorized testing, demonstrations, and
> educational use. A similarity score is not proof of a person’s identity.

## What the project does

For an image containing a detectable face, the `verify` command performs this
workflow:

1. Detects the face and creates a 512-dimensional embedding with InsightFace.
2. Starts a temporary local image server.
3. Creates a temporary Cloudflare Quick Tunnel so Google Lens can access the
   image URL.
4. Sends the image URL to Google Lens through SerpApi.
5. Downloads candidate result thumbnails and compares their faces with the
   input face.
6. Selects the first candidate that passes the similarity threshold.
7. Creates a deterministic SHA-256 fingerprint for the verification record.
8. Stores the record in a local hash-linked blockchain and verifies the block.

The tunnel and local image server are stopped automatically when the command
finishes.

## Requirements

- Python 3.10 or newer
- A working internet connection
- A SerpApi account and API key
- `cloudflared` installed and available on your `PATH`
- A CPU-capable machine (a GPU is not required)
- An image file containing a clear, visible face

## Installation

### 1. Get the code

```bash
git clone https://github.com/odesrani-create/facechain-verifier.git
cd facechain-verifier
```

### 2. Create a virtual environment

Linux and macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install Python packages

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Install Cloudflare `cloudflared`

Install the `cloudflared` command using the instructions for your operating
system in the [Cloudflare documentation](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/).

Check that it is available:

```bash
cloudflared --version
```

### 5. Configure SerpApi

Create a local environment file from the template:

```bash
cp .env.example .env
```

Open `.env` and set your key:

```dotenv
SERPAPI_API_KEY=your_serpapi_key_here
```

Do not commit `.env` or share the API key. The `.gitignore` file is intended
to keep it out of Git.

## Running the project

From the project root, use the following portable command format:

```bash
PYTHONPATH="$PWD/src:$PWD" python run.py verify ./path/to/image.jpg
```

For example:

```bash
PYTHONPATH="$PWD/src:$PWD" python run.py verify ~/Pictures/testing.jpeg
```

The command prints sections for face analysis, web search, face verification,
the best match, and blockchain verification. A successful run ends with a
valid blockchain re-verification message.

### Search without face verification

To run the reverse-image search and print the first results without creating a
blockchain record:

```bash
PYTHONPATH="$PWD/src:$PWD" python run.py search ./path/to/image.jpg
```

### Windows PowerShell

Set the Python import path for the current PowerShell session, then run the
same commands:

```powershell
$env:PYTHONPATH = "$PWD\src;$PWD"
python run.py verify .\path\to\image.jpg
```

## Output and stored data

The verifier creates runtime data under `data/`:

- `data/blockchain.json` contains the local hash-linked blockchain.
- Candidate images may be stored under `data/candidates/` during processing.

Each blockchain block includes an index, timestamp, previous block hash,
verification record, and current block hash. This is a local demonstration of
tamper-evident hashing. It is not a public or decentralized blockchain.

## Project structure

```text
facechain-verifier/
├── config/settings.py       # Loads values from .env
├── run.py                   # Command-line entry point
├── facechain                 # Shell launcher with a configurable project path
├── src/
│   ├── face/                # Face detection and embeddings
│   ├── search/              # Image hosting and SerpApi/Google Lens search
│   ├── verification/        # Candidate downloading and face comparison
│   ├── blockchain/           # Fingerprints and local chain
│   └── cli/                  # Terminal output formatting
├── .env.example             # Configuration template
├── requirements.txt         # Python dependencies
└── data/                    # Runtime output, created as needed
```

## Troubleshooting

### `SERPAPI_API_KEY is missing`

Make sure `.env` exists in the project root and contains a non-empty
`SERPAPI_API_KEY` value. Run the command from the project root.

### `cloudflared: command not found`

Install `cloudflared`, then confirm that `cloudflared --version` works in the
same terminal where you run FaceChain Verifier.

### `ImportError: libGL.so.1`

On Ubuntu or Debian, install the OpenCV system library and retry:

```bash
sudo apt update
sudo apt install libgl1
```

If you cannot install system packages, use an environment that already
provides the OpenCV runtime libraries.

### `Could not obtain Cloudflare tunnel URL`

Check your internet connection, confirm that outbound network access is
allowed, and try again. Quick Tunnels are temporary and can occasionally fail
to start.

### No face is detected

Use a sharper image with a front-facing, visible face and adequate lighting.
The current pipeline expects at least one detectable face.

### No face-verified match is found

Google Lens results change over time, thumbnails may be inaccessible, and face
similarity depends on pose, lighting, resolution, and image quality. A search
result alone does not guarantee a face match.

## Limitations and responsible use

- SerpApi and Google Lens are external services with quotas and possible costs.
- Search results are not guaranteed to be complete, stable, or correct.
- The similarity threshold is a heuristic, not a legal or forensic standard.
- The local blockchain does not provide decentralized trust or immutability.
- The input image is temporarily exposed through a public Quick Tunnel while
  the search request is running.
- Process only images and personal data that you are authorized to use.

## Scope

This repository demonstrates the following proof-of-concept flow:

```text
Face scan -> Web search -> Candidate match -> Face verification
           -> SHA-256 fingerprint -> Local blockchain verification
```

It is a command-line demonstration; no web application is required.

## License

This project is provided for educational and hackathon demonstration purposes.
