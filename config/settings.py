import os
from pathlib import Path

from dotenv import load_dotenv


# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Load .env automatically
ENV_FILE = PROJECT_ROOT / ".env"
load_dotenv(ENV_FILE)


# --------------------------------------------------
# General
# --------------------------------------------------

PROJECT_NAME = os.getenv(
    "PROJECT_NAME",
    "FaceChain Verifier"
)

DEBUG = os.getenv(
    "DEBUG",
    "false"
).lower() == "true"


# --------------------------------------------------
# Search configuration
# --------------------------------------------------

SEARCH_PROVIDER = os.getenv(
    "SEARCH_PROVIDER",
    "serpapi"
).lower()

SERPAPI_API_KEY = os.getenv(
    "SERPAPI_API_KEY",
    ""
)


# --------------------------------------------------
# Image configuration
# --------------------------------------------------

IMAGE_SERVER_PORT = int(
    os.getenv(
        "IMAGE_SERVER_PORT",
        "8000"
    )
)

PUBLIC_IMAGE_URL = os.getenv(
    "PUBLIC_IMAGE_URL",
    ""
)


# --------------------------------------------------
# Blockchain configuration
# --------------------------------------------------

BLOCKCHAIN_PROVIDER = os.getenv(
    "BLOCKCHAIN_PROVIDER",
    "local"
).lower()

BLOCKCHAIN_RPC_URL = os.getenv(
    "BLOCKCHAIN_RPC_URL",
    ""
)

BLOCKCHAIN_PRIVATE_KEY = os.getenv(
    "BLOCKCHAIN_PRIVATE_KEY",
    ""
)


def require(value: str, name: str) -> str:
    """
    Ensure a required configuration value exists.
    """
    if not value:
        raise RuntimeError(
            f"{name} is not configured. "
            f"Add it to {ENV_FILE}"
        )

    return value
