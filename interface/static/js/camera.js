const btn = document.getElementById("start-btn");
const statusText = document.getElementById("status");

btn.addEventListener("click", () => {
    statusText.textContent = "Initializing authentication...";
});
