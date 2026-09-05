# FaceChain Verifier

FaceChain Verifier is a command-line proof-of-concept for **Face Identification & Blockchain Verification**.

It demonstrates this pipeline:

```text
Input Image
    ↓
Face Detection + 512-D Face Encoding
    ↓
Google Lens Reverse Image Search
    ↓
Candidate Social/Web Results
    ↓
Independent Face Similarity Verification
    ↓
SHA-256 Fingerprint
    ↓
Local Blockchain Record
    ↓
Blockchain Re-verification
What it does

Given an input image containing a face, FaceChain Verifier:

Detects and encodes the face using InsightFace.
Publishes the input image temporarily through a Cloudflare Quick Tunnel.
Uses SerpApi with Google Lens for genuine reverse-image search.
Downloads candidate result thumbnails.
Compares candidate faces against the input embedding.
Selects a verified matching result.
Creates a deterministic SHA-256 fingerprint of the verification record.
Stores the fingerprint and record in a local hash-linked blockchain.
Re-verifies the blockchain block to demonstrate tamper detection.
Example
facechain verify ~/Pictures/testing.jpeg

Example result:

FACE ANALYSIS
✓ Face detected
✓ Confidence: 86.24%
✓ Embedding: 512 dimensions

WEB SEARCH
✓ Provider: Google Lens / SerpApi
✓ Visual matches: 60

BEST MATCH
✓ Source: LinkedIn
✓ Similarity: 0.8520
✓ Match: FACE VERIFIED

BLOCKCHAIN
✓ SHA-256 fingerprint generated
✓ Block created
✓ Blockchain hash: VALID
✓ Previous hash: VALID
✓ Re-verification: VALID
Project structure
facechain-verifier/
├── config/
│   └── settings.py
├── src/
│   ├── blockchain/
│   │   ├── fingerprint.py
│   │   └── local_chain.py
│   ├── cli/
│   │   └── ui.py
│   ├── face/
│   │   ├── detector.py
│   │   └── encoder.py
│   ├── search/
│   │   ├── image_server.py
│   │   └── web_search.py
│   └── verification/
│       ├── candidate.py
│       ├── matcher.py
│       └── verifier.py
├── .env.example
├── .gitignore
├── requirements.txt
├── run.py
└── facechain
Requirements
Python 3.10+
Internet connection
SerpApi API key
Cloudflare cloudflared
CPU-capable environment
Installation

Clone the repository:

git clone https://github.com/odesrani-create/facechain-verifier.git
cd facechain-verifier

Create a virtual environment:

python3 -m venv .venv
source .venv/bin/activate

Install Python dependencies:

pip install -r requirements.txt

Install cloudflared and ensure it is available in your PATH.

Create configuration:

cp .env.example .env

Edit .env and add your SerpApi key:

SERPAPI_API_KEY=your_key_here
Usage

Full verification:

facechain verify ./image.jpg

Reverse-image search only:

facechain search ./image.jpg

The verify command automatically starts and stops the temporary local image server and Cloudflare tunnel. No additional terminal windows are required.

Blockchain

The current implementation uses a lightweight local hash-linked blockchain stored in:

data/blockchain.json

Each block contains:

block index
timestamp
previous block hash
verification data
current SHA-256 block hash

The fingerprint is generated from canonical JSON so the same verification record produces the same SHA-256 value.

This is a demonstration blockchain, not a public decentralized network.

Search provider

The current implementation uses:

SerpApi → Google Lens

The search provider is isolated through configuration so another provider can be added later without redesigning the whole pipeline.

Limitations
Google Lens results can change between searches.
Some result thumbnails may be unavailable or protected.
Face similarity is probabilistic and depends on image quality, pose, lighting, and model behavior.
A face similarity match must not be treated as definitive legal identity proof.
The current blockchain is local and is not decentralized.
Cloudflare Quick Tunnels are temporary and are used only to make the input image accessible to the reverse-image-search service.
Search APIs have usage limits and may require a paid plan depending on volume.
Responsible use

Use this project only with images and data you are authorized to process.

For demonstrations, testing, and submissions, prefer your own images or public/consenting test data. Do not use the system to identify private individuals without appropriate authorization.

Hackathon scope

This project implements the required proof-of-concept flow:

Face Scan
→ Web/Social Search
→ Matching Post
→ Face Verification
→ Blockchain Fingerprint
→ Blockchain Verification

No web application is required for the core demonstration.

License

This project is provided for educational and hackathon demonstration purposes.
EOF

Make sure generated runtime data is not committed

cat > .gitignore <<'EOF'
.env
.venv/
pycache/
*.pyc
data/blockchain.json
data/candidates/
EOF

Check what will be committed

git status

Inspect tracked/untracked files

git status --short

Add the final project

git add .gitignore README.md requirements.txt .env.example config run.py facechain src

Commit

git commit -m "Complete FaceChain verification pipeline"

Push

git push origin main


After that, verify:

```bash
git status
git log -1 --oneline

You should end with:

nothing to commit, working tree clean

and your latest commit should be on main.

One important point: your successful 0.8520 face similarity + real LinkedIn result + valid blockchain re-verification is the evidence I would use in the screen recording.
