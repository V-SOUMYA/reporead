from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.github import parse_repo_url

app = FastAPI(title="reporead backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "reporead backend running"}

@app.post("/analyze-repo")
def analyze_repo(payload: dict):
    repo_url = payload.get("repo_url")

    if not repo_url:
        raise HTTPException(status_code=400, detail="repo_url is required")

    try:
        owner, repo = parse_repo_url(repo_url)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "owner": owner,
        "repo": repo,
        "message": "GitHub URL parsed successfully"
    }
