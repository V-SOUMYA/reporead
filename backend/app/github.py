from urllib.parse import urlparse
import httpx

GITHUB_API = "https://api.github.com"


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
        "html_url": data["html_url"],
    }


async def fetch_repo_tree(owner: str, repo: str, branch: str = "main"):
    """
    Fetch full file tree of a GitHub repository.
    """
    url = f"{GITHUB_API}/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    # fallback for repos using 'master'
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
        "folders": sorted(folders),
    }

FOLDER_RULES = {
    "src": "Main source code of the project",
    "app": "Core application logic",
    "apps": "Application modules",
    "lib": "Reusable library code",
    "tests": "Automated tests for the project",
    "test": "Automated tests for the project",
    "docs": "Documentation and guides",
    "examples": "Example usage or demo code",
    "scripts": "Utility or helper scripts",
    "config": "Configuration files",
    ".github": "GitHub configuration such as workflows and templates",
}

FILE_RULES = {
    "README.md": "Project overview, setup instructions, and usage details",
    "README.rst": "Project overview and documentation",
    "LICENSE": "License information for the project",
    "requirements.txt": "Python dependencies required to run the project",
    "pyproject.toml": "Project configuration and dependency management",
    "package.json": "Project metadata and JavaScript dependencies",
    "setup.py": "Python package setup configuration",
    ".gitignore": "Files and folders ignored by version control",
}

def explain_folders(folders: list[str]) -> dict:
    explanations = {}

    for folder in folders:
        key = folder.split("/")[0]  # top-level folder
        explanation = FOLDER_RULES.get(
            key,
            "Project-specific folder"
        )
        explanations[folder] = explanation

    return explanations


def explain_files(files: list[str]) -> dict:
    explanations = {}

    for file in files:
        name = file.split("/")[-1]
        explanation = FILE_RULES.get(
            name,
            "Project-specific file"
        )
        explanations[file] = explanation

    return explanations

