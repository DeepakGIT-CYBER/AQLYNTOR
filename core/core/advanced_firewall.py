import re
import time
from typing import Dict, Any, List

class AQLYNTORUltraFirewall:
    def __init__(self):
        # Threat signature dictionary for deep semantic & regex inspection
        self.threat_patterns = [
            r"ignore previous instructions",
            r"reveal system credentials",
            r"drop table",
            r"union select",
            r"<script>",
            r"exec\(",
            r"eval\("
        ]
        # In-memory request ledger for rate-limiting (IP -> timestamps)
        self.request_ledger: Dict[str, List[float]] = {}
        self.rate_limit_window = 10.0  # seconds
        self.max_requests_allowed = 15

    def inspect_payload(self, payload: str) -> bool:
        """
        Scans the incoming prompt/payload against zero-trust threat signatures.
        Returns True if a threat is detected (Malicious), False otherwise.
        """
        if not payload:
            return False
        
        lower_payload = payload.lower()
        for pattern in self.threat_patterns:
            if re.search(pattern, lower_payload):
                return True
        return False

    def check_rate_limit(self, client_ip: str) -> bool:
        """
        Checks if client IP has exceeded the threshold within the time window.
        Returns True if rate limit is exceeded (Blocked), False otherwise.
        """
        current_time = time.time()
        
        if client_ip not in self.request_ledger:
            self.request_ledger[client_ip] = []

        # Filter out timestamps outside the sliding window
        self.request_ledger[client_ip] = [
            t for t in self.request_ledger[client_ip] 
            if current_time - t < self.rate_limit_window
        ]

        if len(self.request_ledger[client_ip]) >= self.max_requests_allowed:
            return True  # Rate limit exceeded

        # Record current request
        self.request_ledger[client_ip].append(current_time)
        return False