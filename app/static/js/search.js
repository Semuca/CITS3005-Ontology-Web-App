const searchButton = document.getElementById("searchButton");

searchButton.addEventListener("click", () => {
    const tabContainer = document.getElementById("search-tabs");
    const tabs = tabContainer.querySelector('.tabs');
    const selectedTab = tabs.querySelector('.active');

    let query = '?';

    const type = selectedTab.getAttribute("data-rdf-type");
    query += `rdf_type=${type}`;

    window.location.href = query;
});
