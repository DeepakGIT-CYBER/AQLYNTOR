import hashlib
import json
import time

class MerkleAuditTrail:
    def __init__(self):
        self.chain = []
        # Genesis Block
        self.add_log("SYSTEM_INIT", {"status": "AQLYNTOR v3.0 Genesis Block Secured"})

    def add_log(self, action: str, data: dict):
        timestamp = time.time()
        prev_hash = self.chain[-1]["current_hash"] if self.chain else "0" * 64
        
        record = {
            "timestamp": timestamp,
            "action": action,
            "data": data,
            "prev_hash": prev_hash
        }
        
        record_str = json.dumps(record, sort_keys=True)
        current_hash = hashlib.sha256(record_str.encode()).hexdigest()
        
        block = {
            "index": len(self.chain),
            "record": record,
            "current_hash": current_hash
        }
        self.chain.append(block)
        return block

    def verify_integrity(self) -> bool:
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            if current["record"]["prev_hash"] != previous["current_hash"]:
                return False
        return True