import re

class ZeroTrustLLMProxy:
    def __init__(self):
        self.blocked_patterns = [r"password", r"credit_card", r"hack", r"drop table", r"ignore previous instructions"]

    def intercept_and_inspect(self, prompt: str) -> dict:
        for pattern in self.blocked_patterns:
            if re.search(pattern, prompt, re.IGNORECASE):
                return {
                    "version": "v5.0",
                    "action": "BLOCKED_BY_AI_FIREWALL",
                    "reason": f"Detected malicious or sensitive pattern: '{pattern}'"
                }
        return {
            "version": "v5.0",
            "action": "PASSED_SECURE_PROXY",
            "sanitized_prompt": prompt
        }
