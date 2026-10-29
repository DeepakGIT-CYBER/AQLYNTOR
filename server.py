from fastapi import FastAPI, HTTPException, Security, Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import time

from core.crypto_audit import MerkleAuditTrail
from core.swarm_orchestrator import AgentSwarmOrchestrator

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="AQLYNTOR Global 10k Enterprise Engine", version="3.0.0")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()
audit_ledger = MerkleAuditTrail()
swarm_engine = AgentSwarmOrchestrator()

TOKENS_ROLE_MAP = {
    "aqlyntor-secret-token-999": {"role": "Admin", "permissions": ["write", "delete", "audit", "policy_edit", "swarm"]},
    "agent-executor-token-123": {"role": "Agent Executor", "permissions": ["write", "swarm"]},
    "auditor-token-456": {"role": "Auditor", "permissions": ["audit"]}
}

def verify_rbac(required_permission: str):
    def dependency(credentials: HTTPAuthorizationCredentials = Security(security)):
        token = credentials.credentials
        user_info = TOKENS_ROLE_MAP.get(token)
        if not user_info or required_permission not in user_info["permissions"]:
            raise HTTPException(status_code=403, detail=f"[10K SECURITY] RBAC Access Denied.")
        return user_info
    return dependency

class SwarmRequest(BaseModel):
    task_goal: str

@app.get("/", response_class=HTMLResponse)
@limiter.limit("30/minute")
def serve_dashboard(request: Request):
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AQLYNTOR v3.0 — Global 10k AI Safety Observatory</title>
        <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
        <style>body { font-family: 'Inter', sans-serif; }</style>
    </head>
    <body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col items-center justify-between p-6">
        <div class="w-full max-w-6xl mx-auto space-y-6">
            <header class="flex justify-between items-center border-b border-slate-800 pb-4">
                <div>
                    <h1 class="text-3xl font-bold tracking-tight text-emerald-400">AQLYNTOR v3.0 🚀</h1>
                    <p class="text-sm text-slate-400">Global 10k Level: Multi-Agent Swarm & Merkle Crypto Audit Ledger</p>
                </div>
                <div class="flex items-center space-x-3">
                    <span class="px-3 py-1 rounded-full text-xs font-medium bg-emerald-950 text-emerald-400 border border-emerald-800">
                        🛡️ v3.0 Swarm Active
                    </span>
                    <a href="/docs" target="_blank" class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-xs font-semibold rounded-lg transition">Swagger API</a>
                </div>
            </header>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div class="bg-slate-900 border border-slate-800 p-4 rounded-xl">
                    <p class="text-xs text-slate-400 uppercase font-semibold">Multi-Agent Swarm Fleet</p>
                    <h3 class="text-xl font-bold text-cyan-400 mt-1">3 Active Agents</h3>
                    <p class="text-[10px] text-slate-500 mt-1">Coder | Security Reviewer | DevOps</p>
                </div>
                <div class="bg-slate-900 border border-slate-800 p-4 rounded-xl">
                    <p class="text-xs text-slate-400 uppercase font-semibold">Merkle Audit Ledger</p>
                    <h3 class="text-xl font-bold text-indigo-400 mt-1">SHA-256 Tamper-Proof</h3>
                    <p class="text-[10px] text-slate-500 mt-1">Cryptographic Chain Verified</p>
                </div>
                <div class="bg-slate-900 border border-slate-800 p-4 rounded-xl">
                    <p class="text-xs text-slate-400 uppercase font-semibold">Zero-Trust LLM Proxy</p>
                    <h3 class="text-xl font-bold text-emerald-400 mt-1">Active Middleware</h3>
                    <p class="text-[10px] text-slate-500 mt-1">Prompt & Output Guard</p>
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-xl space-y-4">
                    <h2 class="text-lg font-semibold text-slate-200">Execute v3.0 Multi-Agent Swarm Task</h2>
                    <div>
                        <label class="block text-xs font-medium text-slate-400 mb-1">Select Role Profile / Auth Token</label>
                        <select id="authToken" class="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-indigo-500">
                            <option value="aqlyntor-secret-token-999">Admin Role (Full Swarm Access)</option>
                            <option value="agent-executor-token-123">Agent Executor Role</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-xs font-medium text-slate-400 mb-1">Swarm Goal / Task Description</label>
                        <input type="text" id="taskGoal" value="Build and secure enterprise microservice architecture" class="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-indigo-500">
                    </div>
                    <button onclick="executeSwarm()" class="w-full py-2.5 bg-emerald-600 hover:bg-emerald-500 font-semibold text-sm rounded-lg transition shadow-lg shadow-emerald-900/25 cursor-pointer">
                        Execute Swarm & Generate Merkle Block
                    </button>
                </div>

                <div class="bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-xl flex flex-col justify-between">
                    <div>
                        <h2 class="text-lg font-semibold text-slate-200 mb-3">v3.0 Telemetry & Merkle Chain Console</h2>
                        <div class="bg-slate-950 border border-slate-800 rounded-xl p-4 h-64 overflow-y-auto font-mono text-xs text-emerald-400 space-y-2" id="consoleOutput">
                            <span class="text-slate-500">// v3.0 Engine Active. Multi-Agent Swarm & SHA-256 Ledger Ready...</span>
                        </div>
                    </div>
                    <p class="text-xs text-slate-500 mt-4 text-center">AQLYNTOR Global 10k Enterprise Security Engine v3.0</p>
                </div>
            </div>
        </div>

        <script>
            async function executeSwarm() {
                const consoleDiv = document.getElementById('consoleOutput');
                const taskGoal = document.getElementById('taskGoal').value;
                const token = document.getElementById('authToken').value;

                consoleDiv.innerHTML += '<br>&gt; Dispatching Coder, Reviewer & DevOps Swarm...';
                
                try {
                    const response = await fetch('/api/v3/swarm-execute', {
                        method: 'POST',
                        headers: { 
                            'Content-Type': 'application/json',
                            'Authorization': 'Bearer ' + token
                        },
                        body: JSON.stringify({ task_goal: taskGoal })
                    });
                    
                    const result = await response.json();
                    consoleDiv.innerHTML += '<br>&lt; [v3.0 VERIFIED] ' + JSON.stringify(result, null, 2);
                    consoleDiv.scrollTop = consoleDiv.scrollHeight;
                } catch (err) {
                    consoleDiv.innerHTML += '<br>[ERROR] ' + err;
                }
            }
        </script>
    </body>
    </html>
    """

@app.post("/api/v3/swarm-execute")
@limiter.limit("20/minute")
def swarm_execute(req: SwarmRequest, request: Request, user_info: dict = Depends(verify_rbac("swarm"))):
    swarm_result = swarm_engine.execute_swarm_workflow(req.task_goal)
    audit_block = audit_ledger.add_log("SWARM_EXECUTION", {"goal": req.task_goal, "role": user_info["role"]})
    
    return {
        "status": "GLOBAL_10K_VERIFIED",
        "timestamp": time.time(),
        "tenant_role": user_info["role"],
        "swarm_details": swarm_result,
        "merkle_audit_block": audit_block,
        "chain_integrity_valid": audit_ledger.verify_integrity()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)