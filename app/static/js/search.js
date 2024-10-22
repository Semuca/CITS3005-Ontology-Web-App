const searchModal = document.getElementById("searchModal");

const openSearchModalButton = document.getElementById("openSearchButton");
const closeSearchModalButton = document.getElementById("closeSearchButton");

const searchButton = document.getElementById("searchButton");

openSearchModalButton.addEventListener("click", () => {
  searchModal.style.display = "block";
});

closeSearchModalButton.addEventListener("click", () => {
    searchModal.style.display = "none";
});

window.onclick = function(event) {
    if (event.target == searchModal) {
        searchModal.style.display = "none";
    }
}

searchButton.addEventListener("click", () => {
    window.location.href = '/';
});
