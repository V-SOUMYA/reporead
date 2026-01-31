function analyzeRepo() {
  const url = document.getElementById("repo-input").value.trim();
  if (!url) {
    alert("Please enter a GitHub repository URL");
    return;
  }

  // placeholder for backend call
  console.log("Analyzing:", url);
}

async function analyzeRepo() {
  const input = document.getElementById("repo-input");
  const repoUrl = input.value.trim();

  if (!repoUrl) {
    alert("Please enter a GitHub repository URL");
    return;
  }

  // Optional: loading feedback
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

function showLoading() {
  let loader = document.getElementById("loading");
  if (loader) loader.style.display = "block";
}

function hideLoading() {
  let loader = document.getElementById("loading");
  if (loader) loader.style.display = "none";
}

function renderResult(data) {
  const container = document.getElementById("result");
  container.innerHTML = "";

  // Overview
  container.innerHTML += `
    <h2>${data.overview.name}</h2>
    <p>${data.overview.description}</p>
    <p>⭐ ${data.overview.stars} · 🍴 ${data.overview.forks}</p>
    <hr />
  `;

  // Folder explanations
  container.innerHTML += `<h3>Project Structure</h3>`;
  for (const [folder, explanation] of Object.entries(data.explanations.folders)) {
    container.innerHTML += `
      <p><strong>${folder}</strong>: ${explanation}</p>
    `;
  }

  // Contribution ideas
  if (data.contribution_ideas && data.contribution_ideas.length > 0) {
    container.innerHTML += `<h3>Suggested Contributions</h3>`;
    data.contribution_ideas.forEach(idea => {
      container.innerHTML += `
        <div>
          <strong>${idea.title}</strong>
          <p>${idea.description}</p>
        </div>
      `;
    });
  }
}


