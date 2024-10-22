const searchModal = document.getElementById("searchModal");
const openSearchModalButton = document.getElementById("openSearchButton");

openSearchModalButton.addEventListener("click", () => {
    searchModal.style.display = "block";
});


const searchButton = document.getElementById("searchButton");

searchButton.addEventListener("click", () => {
    //TODO: Implement search functionality
    window.location.href = '/';
});
