from urllib.parse import urlparse

def parse_repo_url(repo_url: str):
    """
    Extract owner and repo name from a GitHub URL.
    """
    try:
        parsed = urlparse(repo_url)

        if parsed.netloc != "github.com":
            raise ValueError("Not a GitHub URL")

        parts = parsed.path.strip("/").split("/")

        if len(parts) != 2:
            raise ValueError("Invalid GitHub repository URL")

        owner, repo = parts
        return owner, repo

    except Exception:
        raise ValueError("Invalid GitHub repository URL")


import httpx

GITHUB_API = "https://api.github.com"

async def fetch_repo_metadata(owner: str, repo: str):
    url = f"{GITHUB_API}/repos/{owner}/{repo}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code != 200:
        raise ValueError("Repository not found")

    data = response.json()

    return {
        "name": data["name"],
        "description": data["description"],
        "language": data["language"],
        "stars": data["stargazers_count"],
        "forks": data["forks_count"],
        "html_url": data["html_url"]
    }

import httpx

GITHUB_API = "https://api.github.com"

async def fetch_repo_tree(owner: str, repo: str, branch: str = "main"):
    """
    Fetch full file tree of a GitHub repository.
    """
    url = f"{GITHUB_API}/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    # Some repos still use 'master'
    if response.status_code == 404 and branch == "main":
        return await fetch_repo_tree(owner, repo, branch="master")

    if response.status_code != 200:
        raise ValueError("Could not fetch repository tree")

    data = response.json()

    files = []
    folders = set()

    for item in data["tree"]:
        if item["type"] == "blob":
            files.append(item["path"])
        elif item["type"] == "tree":
            folders.add(item["path"])

    return {
        "files": files,
        "folders": sorted(list(folders))
    }
