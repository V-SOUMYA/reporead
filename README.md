# reporead

**Know where to start before you contribute.**

reporead helps beginners understand a GitHub repository *before* making their first open-source contribution.  
It explains project structure, surfaces beginner-friendly issues, and generates contribution paths when no issues exist.

---

##  Features

-  Analyze any public GitHub repository
-  Explain folders and files in simple terms
-  Detect and preview README
-  Fetch **Good First Issues** (if available)
-  Generate contribution paths when no beginner issues exist
-  Beginner-first, low-overwhelm design

---

##  How it works

1. Paste a GitHub repository URL  
2. Backend fetches metadata, structure, README, and issues  
3. Frontend presents:
   - Project overview
   - Simplified structure
   - Contribution opportunities

If beginner issues exist → they are shown and linked  
If no issues exist → contribution paths are generated

---

## 🛠 Tech Stack

**Frontend**
- HTML
- CSS
- Vanilla JavaScript

**Backend**
- Python
- FastAPI
- httpx (GitHub API)

---

##  Python Version Compatibility (IMPORTANT)

> This project will **NOT** work on all Python versions.

###  Supported
- Python **3.10**
- Python **3.11** (recommended)

###  Not Supported
- Python 3.12
- Python 3.13
- Python 3.14+

FastAPI + Pydantic currently break on Python 3.12+.


