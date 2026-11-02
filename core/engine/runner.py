from pathlib import Path
from core.policies.policy import PolicyGate
from core.verifiers.verifier import OutcomeVerifier


class AqlyntorRunner:
    """Simulation-safe local file runner confined to the policy workspace."""

    def __init__(self, sandbox_dir: str = "./workspace"):
        self.policy = PolicyGate(sandbox_dir=sandbox_dir)
        self.verifier = OutcomeVerifier()

    def run_task(self, task_id: str, action_type: str, target_file: str, sample_content: str = None) -> dict:
        if action_type != "write":
            return {"task_id": task_id, "status": "STOPPED", "reason": "Only write actions are supported."}
        if sample_content is None:
            return {"task_id": task_id, "status": "STOPPED", "reason": "No content supplied; no operation performed."}

        is_allowed, policy_msg = self.policy.validate_action(action_type, target_file)
        if not is_allowed:
            return {"task_id": task_id, "status": "STOPPED", "reason": policy_msg}

        target = Path(target_file).expanduser()
        if not target.is_absolute():
            target = self.policy.sandbox_dir / target
        target = target.resolve()
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(sample_content, encoding="utf-8")
        except OSError as exc:
            return {"task_id": task_id, "status": "FAILED", "reason": f"Write failed: {exc}"}

        verified, verifier_msg = self.verifier.verify_file_exists(str(target))
        if not verified:
            return {"task_id": task_id, "status": "FAILED", "reason": verifier_msg}
        if target.read_text(encoding="utf-8") != sample_content:
            return {"task_id": task_id, "status": "FAILED", "reason": "Verification failed: written content differs from requested content."}
        return {"task_id": task_id, "status": "VERIFIED", "evidence": verifier_msg, "path": str(target)}
