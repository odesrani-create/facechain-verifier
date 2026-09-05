import hashlib
import json


def create_fingerprint(data: dict) -> str:
    """
    Create a deterministic SHA-256 fingerprint
    from verification data.
    """

    canonical = json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )

    return hashlib.sha256(
        canonical.encode("utf-8")
    ).hexdigest()


def verify_fingerprint(
    data: dict,
    expected_fingerprint: str,
) -> bool:

    actual = create_fingerprint(data)

    return actual == expected_fingerprint
