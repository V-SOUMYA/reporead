from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.structure import build_project_structure
from app.github import (
    parse_repo_url,
    fetch_repo_metadata,
    fetch_repo_tree,
    explain_folders,
    explain_files,
    fetch_readme,
    fetch_good_first_issues
)
from app.contributions import generate_contribution_paths

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
        readme = await fetch_readme(owner, repo)
        issues = await fetch_good_first_issues(owner, repo)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    folder_list = tree["folders"][:20]
    file_list = tree["files"][:20]

    project_structure = build_project_structure(folder_list)

    contribution_paths = []
    if len(issues) == 0:
        contribution_paths = generate_contribution_paths(
            folders=folder_list,
            files=file_list,
            readme_exists=readme is not None
        )

    return {
        "overview": metadata,

        "project_structure": {
            "guide": "If you’re new, start with documentation or examples before exploring core code.",
            "groups": project_structure
        },

        "structure": {
            "folders": folder_list,
            "files": file_list
        },

        "explanations": {
            "folders": explain_folders(folder_list),
            "files": explain_files(file_list),
        },

        "readme": {
            "exists": readme is not None,
            "content_preview": readme[:1000] if readme else None
        },

        "issues": {
            "count": len(issues),
            "items": issues
        },

        "contribution_paths": contribution_paths
    }
