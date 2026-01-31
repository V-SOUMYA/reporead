from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="reporead backend")

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # later we can restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "reporead backend running"}

@app.post("/analyze-repo")
def analyze_repo(payload: dict):
    return {
        "message": "Backend is connected",
        "repo_url": payload.get("repo_url")
    }
