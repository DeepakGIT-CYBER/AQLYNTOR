import re

class PolicyGate:
    def __init__(self, restricted_paths=None, forbidden_commands=None):
        self.restricted_paths = restricted_paths or [
            r"C:\\Windows", r"C:\\Program Files", r"/etc", r"/var", r"\\.env"
        ]
        self.forbidden_commands = forbidden_commands or [
            "rm -rf", "del /f /s /q", "format", "drop table", "chmod 777"
        ]

    def validate_action(self, action_type: str, target: str) -> tuple[bool, str]:
        for cmd in self.forbidden_commands:
            if cmd in target.lower():
                return False, f"POLICY VIOLATION: Forbidden command pattern '{cmd}' detected."

        for path in self.restricted_paths:
            if re.search(path, target, re.IGNORECASE):
                return False, f"POLICY VIOLATION: Access to restricted path '{target}' blocked."

        return True, "ALLOWED"
