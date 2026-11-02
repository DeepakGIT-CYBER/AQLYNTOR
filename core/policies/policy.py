from pathlib import Path
from typing import Any


class PolicyGate:
    """Restrict file operations to a dedicated workspace."""

    def __init__(self, sandbox_dir: str = "./workspace"):
        self.sandbox_dir = Path(sandbox_dir).expanduser().resolve()
        self.sandbox_dir.mkdir(parents=True, exist_ok=True)

    def validate_path(self, target_path: str) -> bool:
        if not isinstance(target_path, str) or not target_path.strip():
            return False
        candidate = Path(target_path).expanduser()
        if not candidate.is_absolute():
            candidate = self.sandbox_dir / candidate
        resolved = candidate.resolve()
        return resolved == self.sandbox_dir or self.sandbox_dir in resolved.parents

    def check_action(self, action_type: str, payload: dict[str, Any]) -> tuple[bool, str]:
        if action_type in {"file_write", "file_read"}:
            path = payload.get("path", "")
            if not self.validate_path(path):
                return False, "[POLICY VIOLATION] Access denied: Path outside sandbox boundary."
            return True, "PASSED"
        if action_type in {"destructive_command", "delete", "execute", "deploy", "transfer"}:
            return False, "[POLICY VIOLATION] Destructive or external operations are blocked."
        return False, f"[POLICY VIOLATION] Unsupported action: {action_type}"

    def validate_action(self, action_type: str, target_file: str) -> tuple[bool, str]:
        """Compatibility entry point used by AqlyntorRunner."""
        normalized = {"write": "file_write", "read": "file_read"}.get(action_type, action_type)
        return self.check_action(normalized, {"path": target_file})
