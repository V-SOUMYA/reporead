from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.github import (
    parse_repo_url,
    fetch_repo_metadata,
    fetch_repo_tree,
    explain_folders,
    explain_files
)



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
async def analyze_repo(payload: dict):
    repo_url = payload.get("repo_url")

    if not repo_url:
        raise HTTPException(status_code=400, detail="repo_url is required")

    try:
        owner, repo = parse_repo_url(repo_url)
        metadata = await fetch_repo_metadata(owner, repo)
        tree = await fetch_repo_tree(owner, repo)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    folder_list = tree["folders"][:20]
file_list = tree["files"][:20]

return {
    "overview": metadata,
    "structure": {
        "folders": folder_list,
        "files": file_list,
    },
    "explanations": {
        "folders": explain_folders(folder_list),
        "files": explain_files(file_list),
    }
}

    }






