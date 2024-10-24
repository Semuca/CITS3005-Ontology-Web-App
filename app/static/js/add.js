const addButton = document.getElementById("addButton");
addButton.addEventListener("click", () => {

    const tabContainer = document.getElementById("add-tabs");
    const selectedTabWindow = tabContainer.querySelector('.tab-content.active');

    const rdf_type = selectedTabWindow.getAttribute("data-rdf-type");

    const searchInput = selectedTabWindow.querySelector('#searchInput');
    const label = searchInput.value ? searchInput.value : null;

    fetch('/api/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            rdf_type: rdf_type,
            label: label,
        })
    }).then(response => {
        if (!response.ok) {
            throw new Error(response.statusText);
        }
        return response.text();
    }).then(data => {
        location.reload();
    }).catch(error => {
        console.error(error);
    });
});