import os
from core.policies.policy import PolicyGate
from core.verifiers.verifier import OutcomeVerifier

class AqlyntorRunner:
    def __init__(self):
        self.policy = PolicyGate()
        self.verifier = OutcomeVerifier()

    def run_task(self, task_id: str, action_type: str, target_file: str, sample_content: str = None) -> dict:
        is_allowed, policy_msg = self.policy.validate_action(action_type, target_file)
        if not is_allowed:
            return {"task_id": task_id, "status": "STOPPED", "reason": policy_msg}

        if sample_content is not None:
            os.makedirs(os.path.dirname(target_file) or ".", exist_ok=True)
            with open(target_file, "w", encoding="utf-8") as f:
                f.write(sample_content)

        verified, verifier_msg = self.verifier.verify_file_exists(target_file)
        if not verified:
            return {"task_id": task_id, "status": "RECOVERING", "reason": verifier_msg}

        return {"task_id": task_id, "status": "VERIFIED", "evidence": verifier_msg}
