const addModal = document.getElementById("deleteModal");
const openDeleteModalButtons = document.getElementsByClassName("openDeleteButton");

for (let openDeleteModalButton of openDeleteModalButtons) {
    openDeleteModalButton.addEventListener("click", (event) => {
        addModal.style.display = "block";
        event.preventDefault();
    });
}


const addButton = document.getElementById("deleteButton");

addButton.addEventListener("click", () => {
    //TODO: Implement delete functionality
    window.location.href = '/';
});