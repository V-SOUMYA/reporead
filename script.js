/* ===============================
   MAIN ACTION
================================ */

async function analyzeRepo() {
  const input = document.getElementById("repo-input");
  const repoUrl = input.value.trim();

  if (!repoUrl) {
    alert("Please enter a GitHub repository URL");
    return;
  }

  showLoading();

  try {
    const response = await fetch("http://localhost:8000/analyze-repo", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ repo_url: repoUrl })
    });

    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.detail || "Something went wrong");
    }

    const data = await response.json();
    renderResult(data);

  } catch (error) {
    alert(error.message);
  } finally {
    hideLoading();
  }
}

/* ===============================
   LOADING STATE
================================ */

function showLoading() {
  const loader = document.getElementById("loading");
  if (loader) loader.style.display = "block";
}

function hideLoading() {
  const loader = document.getElementById("loading");
  if (loader) loader.style.display = "none";
}

/* ===============================
   RENDER RESULT (ORCHESTRATOR)
================================ */

function renderResult(data) {
  const container = document.getElementById("result");
  container.innerHTML = "";

  /* ---------- OVERVIEW ---------- */
  container.innerHTML += `
    <div class="card glow-card">
      <div class="card-content">
        <h2>${data.overview.name}</h2>
        <p>${data.overview.description}</p>
        <p class="muted">
          ⭐ ${data.overview.stars} · 🍴 ${data.overview.forks}
        </p>
      </div>
    </div>
  `;

  /* ---------- PROJECT STRUCTURE ---------- */
  if (data.explanations?.folders) {
    const folders = Object.entries(data.explanations.folders)
      .slice(0, 6)
      .map(
        ([folder, explanation]) =>
          `<p><strong>${folder}</strong> — <span class="muted">${explanation}</span></p>`
      )
      .join("");

    container.innerHTML += `
      <div class="card glow-card">
        <div class="card-content">
          <h3>📁 Project Structure</h3>
          <p class="muted">Start by understanding where things live</p>
          ${folders}
        </div>
      </div>
    `;
  }

  /* ---------- CONTRIBUTION PATHS (FIRSTPATCH STYLE) ---------- */
  if (
    data.issues?.count === 0 &&
    data.contribution_ideas &&
    data.contribution_ideas.length > 0
  ) {
    renderContributionPaths(data.contribution_ideas);
  }
}

/* ===============================
   CONTRIBUTION PATH CARDS
================================ */

function renderContributionPaths(paths) {
  const container = document.getElementById("result");

  container.innerHTML += `
    <div class="section-header">
      <h3>✨ Contribution Paths</h3>
      <p class="muted">Beginner-friendly ways to get started</p>
    </div>
  `;

  paths.forEach(path => {
    container.innerHTML += `
      <div class="card glow-card contribution-card">
        <div class="card-content">

          <div class="card-header">
            <h4>${path.title}</h4>
            <span class="badge ${path.difficulty}">
              ${path.difficulty}
            </span>
          </div>

          <p class="muted">${path.context}</p>

          <div class="steps">
            <strong>Suggested steps</strong>
            <ol>
              ${path.suggested_steps.map(step => `<li>${step}</li>`).join("")}
            </ol>
          </div>

          <div class="files">
            <strong>Relevant files</strong>
            <div class="file-tags">
              ${path.files.map(file => `<span>${file}</span>`).join("")}
            </div>
          </div>

          <div class="meta muted">
            ⏱ ${path.estimated_time} · ${path.category}
          </div>

        </div>
      </div>
    `;
  });
}
