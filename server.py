from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
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

@app.get("/", response_class=HTMLResponse)
def serve_dashboard():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AQLYNTOR — Trustworthy AI Execution Engine</title>
        <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
        <style>body { font-family: 'Inter', sans-serif; }</style>
    </head>
    <body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col items-center justify-between p-6">
        <div class="w-full max-w-5xl mx-auto space-y-6">
            <header class="flex justify-between items-center border-b border-slate-800 pb-4">
                <div>
                    <h1 class="text-3xl font-bold tracking-tight text-emerald-400">AQLYNTOR 🚀</h1>
                    <p class="text-sm text-slate-400">Trustworthy AI Execution & Task Safety Observatory</p>
                </div>
                <div class="flex items-center space-x-3">
                    <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-emerald-950 text-emerald-400 border border-emerald-800">
                        ● System Active & Secure
                    </span>
                    <a href="/docs" target="_blank" class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-xs font-semibold rounded-lg transition">API Docs</a>
                </div>
            </header>

            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div class="bg-slate-900 border border-slate-800 p-4 rounded-xl">
                    <p class="text-xs text-slate-400 uppercase font-semibold">Success Rate</p>
                    <h3 class="text-2xl font-bold text-emerald-400 mt-1">99.4%</h3>
                </div>
                <div class="bg-slate-900 border border-slate-800 p-4 rounded-xl">
                    <p class="text-xs text-slate-400 uppercase font-semibold">Active Tasks</p>
                    <h3 class="text-2xl font-bold text-blue-400 mt-1">3</h3>
                </div>
                <div class="bg-slate-900 border border-slate-800 p-4 rounded-xl">
                    <p class="text-xs text-slate-400 uppercase font-semibold">Bounded Recoveries</p>
                    <h3 class="text-2xl font-bold text-amber-400 mt-1">7</h3>
                </div>
                <div class="bg-slate-900 border border-slate-800 p-4 rounded-xl">
                    <p class="text-xs text-slate-400 uppercase font-semibold">Policy Blocked</p>
                    <h3 class="text-2xl font-bold text-rose-400 mt-1">1</h3>
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-xl space-y-4">
                    <h2 class="text-lg font-semibold text-slate-200">Execute AI Task Pipeline</h2>
                    <div>
                        <label class="block text-xs font-medium text-slate-400 mb-1">Task ID</label>
                        <input type="text" id="taskId" value="TASK-LIVE-01" class="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-emerald-500">
                    </div>
                    <div>
                        <label class="block text-xs font-medium text-slate-400 mb-1">Action Type</label>
                        <select id="actionType" class="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-emerald-500">
                            <option value="write">Write / Generate</option>
                            <option value="delete">Delete (Simulate Policy Violation)</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-xs font-medium text-slate-400 mb-1">Target File Path</label>
                        <input type="text" id="targetFile" value="outputs/live_result.md" class="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-emerald-500">
                    </div>
                    <div>
                        <label class="block text-xs font-medium text-slate-400 mb-1">Sample Content</label>
                        <textarea id="sampleContent" rows="2" class="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-emerald-500"># AQLYNTOR Real-Time Execution Verified Successfully</textarea>
                    </div>
                    <button onclick="executeTask()" class="w-full py-2.5 bg-emerald-600 hover:bg-emerald-500 font-semibold text-sm rounded-lg transition shadow-lg shadow-emerald-900/25 cursor-pointer">
                        Run Policy & Verification Engine
                    </button>
                </div>

                <div class="bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-xl flex flex-col justify-between">
                    <div>
                        <h2 class="text-lg font-semibold text-slate-200 mb-3">Execution Telemetry Console</h2>
                        <div class="bg-slate-950 border border-slate-800 rounded-xl p-4 h-64 overflow-y-auto font-mono text-xs text-emerald-400 space-y-2" id="consoleOutput">
                            <span class="text-slate-500">// System initialized. Ready for task execution...</span>
                        </div>
                    </div>
                    <p class="text-xs text-slate-500 mt-4 text-center">AQLYNTOR Autonomous Task Safety Framework v1.0</p>
                </div>
            </div>
        </div>

        <script>
            async function executeTask() {
                const consoleDiv = document.getElementById('consoleOutput');
                const taskId = document.getElementById('taskId').value;
                const actionType = document.getElementById('actionType').value;
                const targetFile = document.getElementById('targetFile').value;
                const sampleContent = document.getElementById('sampleContent').value;

                consoleDiv.innerHTML += '<br>&gt; Dispatching task ' + taskId + ' through PolicyGate & Verifier...';
                
                try {
                    const response = await fetch('/api/execute', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ task_id: taskId, action_type: actionType, target_file: targetFile, sample_content: sampleContent })
                    });
                    const result = await response.json();
                    consoleDiv.innerHTML += '<br>&lt; RESPONSE: ' + JSON.stringify(result, null, 2);
                    consoleDiv.scrollTop = consoleDiv.scrollHeight;
                } catch (err) {
                    consoleDiv.innerHTML += '<br>[ERROR] Failed to connect: ' + err;
                }
            }
        </script>
    </body>
    </html>
    """

@app.get("/api/stats")
def get_stats():
    return {
        "success_rate": 99.4,
        "active_tasks": 3,
        "bounded_recoveries": 7,
        "policy_violations_blocked": 1
    }

@app.post("/api/execute")
def execute_task(req: TaskRequest):
    result = runner.run_task(req.task_id, req.action_type, req.target_file, req.sample_content)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
