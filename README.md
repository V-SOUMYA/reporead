# reporead

**Read a repo before you touch it.**

reporead is a beginner-friendly tool that helps you understand a GitHub repository *before* making your first open-source contribution.

Instead of feeling overwhelmed by folders, files, and unfamiliar codebases, reporead explains what a project contains, where beginners should start, and how they can contribute safely.

---

## ✨ What reporead does

Given a public GitHub repository URL, reporead:

- 🔍 Fetches repository metadata (name, stars, forks, language)
- 🗂 Analyzes the project’s folder and file structure
- 🧭 Explains what folders and files are used for (in simple terms)
- 📄 Detects and previews the README
- 🐛 Fetches **Good First Issues** if they exist
- 💡 Generates **AI-guided contribution paths** when no beginner issues exist

The goal is to **reduce confusion**, **lower the barrier to entry**, and help new contributors start with confidence.

---

## 🧠 How it works

1. You paste a GitHub repository URL  
2. The backend fetches metadata, structure, README, and issues using GitHub APIs  
3. The frontend presents:
   - A clean project overview
   - Simplified project structure
   - Beginner-friendly contribution opportunities

### Contribution logic
- If **Good First Issues exist** → show and link them
- If **no beginner issues exist** → generate contribution paths (docs, examples, tests, etc.)

---

## 🛠 Tech Stack

### Frontend
- HTML
- CSS
- Vanilla JavaScript

### Backend
- Python
- FastAPI
- httpx (for async GitHub API calls)

---

## ⚠️ Python Version Compatibility (IMPORTANT)

> **reporead will NOT run on all Python versions.**

### ✅ Supported versions
- **Python 3.10**
- **Python 3.11 (recommended)**

### ❌ Not supported
- Python 3.12
- Python 3.13
- Python 3.14+

FastAPI currently depends on Pydantic internals that break on Python 3.12+.

If you see errors like:

