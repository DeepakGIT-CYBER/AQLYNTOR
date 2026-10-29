import pytest
from core.policies.policy import PolicyGate
from core.verifiers.verifier import OutcomeVerifier
from core.engine.runner import AqlyntorRunner

def test_policy_gate_allowed():
    policy = PolicyGate()
    allowed, _ = policy.validate_action("write", "outputs/test.md")
    assert allowed == True

def test_policy_gate_blocked():
    policy = PolicyGate()
    allowed, _ = policy.validate_action("delete", "C:\\Windows\\System32\\cmd.exe")
    assert allowed == False

def test_verifier_file_missing():
    verifier = OutcomeVerifier()
    success, _ = verifier.verify_file_exists("non_existent_file_12345.md")
    assert success == False

def test_runner_execution():
    runner = AqlyntorRunner()
    res = runner.run_task("TASK-PRO-01", "write", "outputs/pro_summary.md", "# AQLYNTOR Pro Verification Passed")
    assert res["status"] == "VERIFIED"
