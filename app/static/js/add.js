const addModal = document.getElementById("addModal");
const openAddModalButton = document.getElementById("openAddButton");

openAddModalButton.addEventListener("click", () => {
    addModal.style.display = "block";
});


const addButton = document.getElementById("addButton");
addButton.addEventListener("click", () => {
    //TODO: Implement add functionality
    window.location.href = '/';
});