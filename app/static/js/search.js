const limitSelectors = document.querySelectorAll('.limit-selector');

limitSelectors.forEach((limitSelector) => {
    const urlObj = new URL(window.location.href, window.location.origin);

    urlObj.searchParams.set('limit', limitSelector.textContent);

    limitSelector.href = urlObj.toString();
});

const searchButton = document.getElementById("searchButton");

searchButton.addEventListener("click", () => {
    const tabContainer = document.getElementById("search-tabs");
    const selectedTabWindow = tabContainer.querySelector('.tab-content.active');

    const query = [];

    const type = selectedTabWindow.getAttribute("data-rdf-type");
    query.push(`rdf_type=props:${type}`);

    const searchInput = selectedTabWindow.querySelector('#searchInput');
    if (searchInput.value) {
        query.push(`name=${searchInput.value}`);
    }

    const queryString = `?${query.join('&')}`;

    window.location.href = queryString;
});
