from pathlib import Path

class PolicyGate:
    def __init__(self, sandbox_dir: str = "./workspace"):
        self.sandbox_dir = Path(sandbox_dir).resolve()
        self.sandbox_dir.mkdir(parents=True, exist_ok=True)

    def validate_path(self, target_path: str) -> bool:
        resolved_path = Path(target_path).resolve()
        return self.sandbox_dir in resolved_path.parents or resolved_path == self.sandbox_dir

    def check_action(self, action_type: str, payload: dict) -> tuple[bool, str]:
        if action_type in ["file_write", "file_read"]:
            path = payload.get("path", "")
            if not self.validate_path(path):
                return False, "[POLICY VIOLATION] Access denied: Path outside sandbox boundary."
        if action_type == "destructive_command":
            return False, "[POLICY VIOLATION] Destructive system operations are blocked by default."
        return True, "PASSED"