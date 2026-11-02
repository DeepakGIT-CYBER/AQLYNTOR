from core.policies.policy import PolicyGate
from core.verifiers.verifier import OutcomeVerifier
from core.engine.runner import AqlyntorRunner


def test_policy_gate_allows_workspace_write(tmp_path):
    policy = PolicyGate(str(tmp_path / "workspace"))
    allowed, _ = policy.validate_action("write", "outputs/result.md")
    assert allowed is True


def test_policy_gate_blocks_path_traversal(tmp_path):
    policy = PolicyGate(str(tmp_path / "workspace"))
    allowed, _ = policy.validate_action("write", "../outside.txt")
    assert allowed is False


def test_policy_gate_blocks_destructive_action(tmp_path):
    policy = PolicyGate(str(tmp_path / "workspace"))
    allowed, _ = policy.validate_action("delete", "important.txt")
    assert allowed is False


def test_policy_gate_rejects_unknown_action(tmp_path):
    policy = PolicyGate(str(tmp_path / "workspace"))
    allowed, _ = policy.validate_action("shell", "anything")
    assert allowed is False


def test_verifier_file_missing(tmp_path):
    verifier = OutcomeVerifier()
    success, _ = verifier.verify_file_exists(str(tmp_path / "missing.md"))
    assert success is False


def test_runner_writes_and_verifies_exact_content(tmp_path):
    runner = AqlyntorRunner(sandbox_dir=str(tmp_path / "workspace"))
    result = runner.run_task("TASK-001", "write", "outputs/result.md", "# Verified")
    assert result["status"] == "VERIFIED"
    assert (tmp_path / "workspace" / "outputs" / "result.md").read_text(encoding="utf-8") == "# Verified"


def test_runner_refuses_outside_sandbox(tmp_path):
    runner = AqlyntorRunner(sandbox_dir=str(tmp_path / "workspace"))
    result = runner.run_task("TASK-002", "write", "../outside.txt", "unsafe")
    assert result["status"] == "STOPPED"
    assert not (tmp_path / "outside.txt").exists()


def test_runner_refuses_missing_content(tmp_path):
    runner = AqlyntorRunner(sandbox_dir=str(tmp_path / "workspace"))
    result = runner.run_task("TASK-003", "write", "result.md")
    assert result["status"] == "STOPPED"
