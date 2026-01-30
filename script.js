function analyzeRepo() {
  const url = document.getElementById("repo-input").value.trim();
  if (!url) {
    alert("Please enter a GitHub repository URL");
    return;
  }

  // placeholder for backend call
  console.log("Analyzing:", url);
}
