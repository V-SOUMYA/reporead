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
