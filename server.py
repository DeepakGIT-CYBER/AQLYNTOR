from fastapi import FastAPI, HTTPException
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
