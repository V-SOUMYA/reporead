async function analyzeRepo() {
  const repoUrl = document.getElementById("repo-input").value.trim();
  if (!repoUrl) {
    alert("Please enter a GitHub repository URL");
    return;
  }

  showLoading();

  try {
    const response = await fetch("http://localhost:8000/analyze-repo", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ repo_url: repoUrl })
    });

    const data = await response.json();
    renderResult(data);

  } catch (err) {
    alert(err.message);
  } finally {
    hideLoading();
  }
}

function showLoading() {
  document.getElementById("loading").style.display = "block";
}
function hideLoading() {
  document.getElementById("loading").style.display = "none";
}

function renderResult(data) {
  const container = document.getElementById("result");
  container.innerHTML = "";

  // OVERVIEW
  container.innerHTML += `
    <div class="card glow-card">
      <div class="card-content">
        <h2>${data.overview.name}</h2>
        <p>${data.overview.description}</p>
        <p class="muted">⭐ ${data.overview.stars} · 🍴 ${data.overview.forks}</p>
      </div>
    </div>
  `;

  // PROJECT STRUCTURE
  const folders = Object.entries(data.explanations.folders)
    .slice(0, 6)
    .map(
      ([f, e]) => `<p><strong>${f}</strong> — <span class="muted">${e}</span></p>`
    )
    .join("");

  container.innerHTML += `
    <div class="card glow-card">
      <div class="card-content">
        <h3>📁 Project Structure</h3>
        ${folders}
      </div>
    </div>
  `;

  // EXISTING ISSUES (CLICKABLE)
  if (data.issues.count > 0) {
    container.innerHTML += `
      <div class="card glow-card">
        <div class="card-content">
          <h3>🐛 Beginner-friendly Issues</h3>
          ${data.issues.items.map(issue => `
            <a href="${issue.html_url}" target="_blank" class="issue-link">
              #${issue.number} — ${issue.title}
            </a>
          `).join("")}
        </div>
      </div>
    `;
  }

  // CONTRIBUTION PATHS (NO ISSUES)
  if (
    data.issues.count === 0 &&
    data.contribution_paths &&
    data.contribution_paths.length > 0
  ) {
    renderContributionPaths(data.contribution_paths);
  }
}

function renderContributionPaths(paths) {
  const container = document.getElementById("result");

  container.innerHTML += `
    <h3 style="margin-top:40px">✨ Contribution Paths</h3>
  `;

  paths.forEach(path => {
    container.innerHTML += `
      <div class="card glow-card">
        <div class="card-content">
          <h4>${path.title}</h4>
          <p class="muted">${path.context}</p>

          <strong>Suggested steps</strong>
          <ol>
            ${path.suggested_steps.map(s => `<li>${s}</li>`).join("")}
          </ol>

          <p class="muted">
            📁 ${path.files.join(", ")} · ⏱ ${path.estimated_time}
          </p>
        </div>
      </div>
    `;
  });
}
