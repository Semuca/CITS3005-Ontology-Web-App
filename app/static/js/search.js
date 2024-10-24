const url = new URL(window.location.href, window.location.origin);

const pageSize = parseInt(url.searchParams.get('pageSize')) || 20;
const pageSizeSelectors = document.querySelectorAll('.limit-selector');

pageSizeSelectors.forEach((pageSizeSelector) => {
    const _url = new URL(window.location.href, window.location.origin);

    _url.searchParams.set('pageSize', pageSizeSelector.textContent);

    pageSizeSelector.href = _url.toString();
});

const pageNumber = parseInt(url.searchParams.get('page')) || 1;

const previousPageButton = document.getElementById('previousPageButton');
if (pageNumber > 1) {
    const _url = new URL(window.location.href, window.location.origin);
    _url.searchParams.set('page', pageNumber - 1);
    previousPageButton.href = _url.toString();
} else {
    previousPageButton.remove();
}

const nextPageButton = document.getElementById('nextPageButton');
if (document.getElementsByClassName('link').length === pageSize) {
    const _url = new URL(window.location.href, window.location.origin);
    _url.searchParams.set('page', pageNumber + 1);
    nextPageButton.href = _url.toString();
} else {
    nextPageButton.remove();
}


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
