const addModal = document.getElementById("addModal");
const openAddModalButton = document.getElementById("openAddButton");

openAddModalButton.addEventListener("click", () => {
    addModal.style.display = "block";
});


const addButton = document.getElementById("addButton");
addButton.addEventListener("click", () => {
    //TODO: Implement add functionality
    
    fetch('/api/', {
        method: 'POST',
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