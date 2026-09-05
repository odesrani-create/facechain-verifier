import hashlib
import json
import time
from pathlib import Path


class LocalBlockchain:
    """
    Lightweight local blockchain used for tamper-evident
    verification records.

    Each block contains:
    - block index
    - timestamp
    - previous block hash
    - transaction data
    - current block hash
    """

    def __init__(
        self,
        chain_file: str = "data/blockchain.json",
    ):
        self.chain_file = Path(chain_file)

        self.chain_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if not self.chain_file.exists():
            self._create_genesis_block()

    def _calculate_hash(self, block: dict) -> str:
        data = {
            key: value
            for key, value in block.items()
            if key != "hash"
        }

        encoded = json.dumps(
            data,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")

        return hashlib.sha256(encoded).hexdigest()

    def _create_genesis_block(self):
        genesis = {
            "index": 0,
            "timestamp": time.time(),
            "previous_hash": "0" * 64,
            "data": {
                "type": "genesis",
                "message": "FaceChain Verifier Genesis Block",
            },
        }

        genesis["hash"] = self._calculate_hash(
            genesis
        )

        self._save_chain([genesis])

    def _load_chain(self) -> list[dict]:
        with self.chain_file.open(
            "r",
            encoding="utf-8",
        ) as file:
            return json.load(file)

    def _save_chain(self, chain: list[dict]):
        with self.chain_file.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                chain,
                file,
                indent=2,
            )

    def add_record(self, data: dict) -> dict:
        chain = self._load_chain()

        previous = chain[-1]

        block = {
            "index": len(chain),
            "timestamp": time.time(),
            "previous_hash": previous["hash"],
            "data": data,
        }

        block["hash"] = self._calculate_hash(
            block
        )

        chain.append(block)

        self._save_chain(chain)

        return block

    def verify_block(self, block_index: int) -> dict:
        chain = self._load_chain()

        if block_index < 0 or block_index >= len(chain):
            raise IndexError(
                "Blockchain block does not exist."
            )

        block = chain[block_index]

        calculated_hash = self._calculate_hash(
            block
        )

        hash_valid = (
            calculated_hash == block["hash"]
        )

        previous_valid = True

        if block_index > 0:
            previous = chain[block_index - 1]

            previous_valid = (
                block["previous_hash"]
                == previous["hash"]
            )

        return {
            "block_index": block_index,
            "stored_hash": block["hash"],
            "calculated_hash": calculated_hash,
            "hash_valid": hash_valid,
            "previous_hash_valid": previous_valid,
            "verified": (
                hash_valid
                and previous_valid
            ),
        }

    def verify_chain(self) -> dict:
        chain = self._load_chain()

        results = []

        for index in range(len(chain)):
            results.append(
                self.verify_block(index)
            )

        valid = all(
            item["verified"]
            for item in results
        )

        return {
            "valid": valid,
            "blocks": len(chain),
            "results": results,
        }
