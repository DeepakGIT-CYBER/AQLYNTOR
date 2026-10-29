import os

files = {
    "requirements.txt": """fastapi==0.110.0
uvicorn==0.28.0
pydantic==2.6.4
pytest==8.1.0
""",
    
    "core/policies/policy.py": '''import re

class PolicyGate:
    def __init__(self, restricted_paths=None, forbidden_commands=None):
        self.restricted_paths = restricted_paths or [
            r"C:\\Windows", r"C:\\Program Files", r"/etc", r"/var", r"\.env"
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
''',

    "core/verifiers/verifier.py": '''import os

class OutcomeVerifier:
    def verify_file_exists(self, file_path: str, min_bytes: int = 1) -> tuple[bool, str]:
        if not os.path.exists(file_path):
            return False, f"VERIFICATION FAILED: Target file '{file_path}' does not exist."
        
        file_size = os.path.getsize(file_path)
        if file_size < min_bytes:
            return False, f"VERIFICATION FAILED: File size ({file_size} bytes) is below threshold."

        return True, f"VERIFIED: File '{file_path}' exists ({file_size} bytes)."

    def verify_content_contains(self, file_path: str, required_keyword: str) -> tuple[bool, str]:
        exists, msg = self.verify_file_exists(file_path)
        if not exists:
            return False, msg

        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        if required_keyword not in content:
            return False, f"VERIFICATION FAILED: Required signature '{required_keyword}' missing."

        return True, f"VERIFIED: Found required signature '{required_keyword}'."
''',

    "core/engine/runner.py": '''import os
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
''',

    "server.py": '''from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from core.engine.runner import AqlyntorRunner

app = FastAPI(title="AQLYNTOR Engine API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

runner = AqlyntorRunner()

class TaskRequest(BaseModel):
    task_id: str
    action_type: str
    target_file: str
    sample_content: str = None

@app.get("/api/stats")
def get_stats():
    return {
        "success_rate": 88,
        "active_tasks": 2,
        "bounded_recoveries": 4,
        "policy_violations_blocked": 1
    }

@app.post("/api/execute")
def execute_task(req: TaskRequest):
    result = runner.run_task(req.task_id, req.action_type, req.target_file, req.sample_content)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
'''
}

def build_project():
    print("[AQLYNTOR] Building complete architecture...")
    for filepath, content in files.items():
        dir_name = os.path.dirname(filepath)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[Created] -> {filepath}")
    print("[SUCCESS] All core files generated successfully!")

if __name__ == "__main__":
    build_project()
'''.strip()

print("File setup_full.py written successfully!")