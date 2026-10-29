import hashlib
import json
import time

class P2PBlockchainLedger:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        block = {"index": 0, "timestamp": time.time(), "data": "Genesis P2P Block", "prev_hash": "0"*64}
        block["hash"] = hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()
        self.chain.append(block)

    def add_decentralized_record(self, agent_action: str) -> dict:
        prev_block = self.chain[-1]
        new_block = {
            "index": len(self.chain),
            "timestamp": time.time(),
            "agent_action": agent_action,
            "prev_hash": prev_block["hash"]
        }
        new_block["hash"] = hashlib.sha256(json.dumps(new_block, sort_keys=True).encode()).hexdigest()
        self.chain.append(new_block)
        return {"version": "v6.0", "p2p_block_added": new_block, "chain_length": len(self.chain)}
