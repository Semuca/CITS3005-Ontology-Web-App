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
    fetch('/api/', {
        method: 'DELETE',
    }).then(response => {
        if (!response.ok) {
            throw new Error(response.statusText);
        }
        return response.text();
    }).then(data => {
        console.log(data);
    }).catch(error => {
        console.error(error);
    });
    // window.location.href = '/';
});