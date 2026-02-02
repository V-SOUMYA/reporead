def generate_contribution_paths(folders, files, readme_exists):
    contributions = []

    if "docs" in folders or readme_exists:
        contributions.append({
            "id": "docs",
            "title": "Improve Project Documentation",
            "difficulty": "easy",
            "category": "Documentation",
            "estimated_time": "1–2 hours",
            "context": (
                "Good documentation helps new users and contributors "
                "understand the project quickly."
            ),
            "suggested_steps": [
                "Read the README from start to finish",
                "Identify unclear setup or usage steps",
                "Improve explanations or add examples",
                "Fix typos or broken links"
            ],
            "files": ["README.md", "docs/"]
        })

    if "examples" in folders:
        contributions.append({
            "id": "examples",
            "title": "Improve Example Code",
            "difficulty": "easy",
            "category": "Examples",
            "estimated_time": "2–4 hours",
            "context": (
                "Examples help contributors understand how the project is used "
                "in real-world scenarios."
            ),
            "suggested_steps": [
                "Run existing examples",
                "Add comments explaining each step",
                "Simplify complex logic",
                "Ensure examples still work"
            ],
            "files": ["examples/"]
        })

    if "tests" in folders:
        contributions.append({
            "id": "tests",
            "title": "Add or Improve Tests",
            "difficulty": "medium",
            "category": "Testing",
            "estimated_time": "1 day",
            "context": (
                "Tests improve confidence in changes and prevent regressions."
            ),
            "suggested_steps": [
                "Review existing tests",
                "Identify untested areas",
                "Add new test cases",
                "Improve test naming and clarity"
            ],
            "files": ["tests/"]
        })

    return contributions

