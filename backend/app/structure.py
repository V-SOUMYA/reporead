from collections import defaultdict

def build_project_structure(folders, files=None):
    sections = defaultdict(list)

    for folder in folders:
        f = folder.lower()

        if any(x in f for x in ["src", "frontend", "components", "pages", "ui"]):
            section = "Frontend"

        elif any(x in f for x in ["api", "backend", "server", "routes"]):
            section = "Backend"

        elif any(x in f for x in ["db", "database", "models"]):
            section = "Database"

        elif any(x in f for x in ["styles", "css", "scss"]):
            section = "Styling"

        elif any(x in f for x in ["docs"]):
            section = "Documentation"

        elif any(x in f for x in ["tests", "examples", "sample"]):
            section = "Examples & Tests"

        else:
            section = "Other"

        sections[section].append({
            "path": folder,
            "purpose": infer_folder_purpose(folder)
        })

    return [
        {
            "id": key.lower().replace(" ", "_"),
            "title": key,
            "description": section_description(key),
            "folders": value
        }
        for key, value in sections.items()
    ]


def infer_folder_purpose(folder):
    name = folder.lower()

    if "pages" in name:
        return "Page-level components representing screens or routes"

    if "components" in name:
        return "Reusable UI components used across pages"

    if "api" in name:
        return "API endpoints handling requests and responses"

    if "db" in name:
        return "Database models and persistence logic"

    if "styles" in name:
        return "Styling and layout definitions"

    if "docs" in name:
        return "Project documentation and guides"

    return "Supporting project code"


def section_description(section):
    return {
        "Frontend": "User-facing interface and interaction logic",
        "Backend": "Server-side logic and request handling",
        "Database": "Data models and storage layer",
        "Styling": "Visual appearance and layout",
        "Documentation": "Guides and explanations for users and contributors",
        "Examples & Tests": "Sample usage and automated tests",
        "Other": "Supporting or configuration code"
    }.get(section, "")
