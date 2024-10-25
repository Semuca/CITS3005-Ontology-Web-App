const url = new URL(window.location.href, window.location.origin);

// Set up page selectors
const pageSize = parseInt(url.searchParams.get('pageSize')) || 20;
const pageSizeSelectors = document.querySelectorAll('.limit-selector');

pageSizeSelectors.forEach((pageSizeSelector) => {
    const _url = new URL(window.location.href, window.location.origin);

    _url.searchParams.set('pageSize', pageSizeSelector.textContent);

    pageSizeSelector.href = _url.toString();
});

const pageNumber = parseInt(url.searchParams.get('page')) || 1;

// Set up previous page button
const previousPageButton = document.getElementById('previousPageButton');
if (previousPageButton) {
    if (pageNumber > 1) {
        const _url = new URL(window.location.href, window.location.origin);
        _url.searchParams.set('page', pageNumber - 1);
        previousPageButton.href = _url.toString();
    } else {
        previousPageButton.remove();
    }
}

// Set up next page button
const nextPageButton = document.getElementById('nextPageButton');
if (nextPageButton) {
    if (document.getElementsByClassName('link').length === pageSize) {
        const _url = new URL(window.location.href, window.location.origin);
        _url.searchParams.set('page', pageNumber + 1);
        nextPageButton.href = _url.toString();
    } else {
        nextPageButton.remove();
    }
}


const searchButton = document.getElementById("searchButton");

searchButton.addEventListener("click", () => {
    const _url = new URL(window.location.href, window.location.origin);
    _url.pathname = '/';
    _url.search = '';

    const tabContainer = document.getElementById("search-tabs");
    const selectedTabWindow = tabContainer.querySelector('.tab-content.active');

    const type = selectedTabWindow.getAttribute("data-rdf-type");
    _url.searchParams.set('rdf_type', `ifixthat:${type}`);

    const propertyInputs =
		selectedTabWindow.querySelectorAll(".property-input");

    propertyInputs.forEach((input) => {
		const property = input.getAttribute("data-property");
		const value = input.value;
		if (value) {
            _url.searchParams.set(property, value);
		}
	});

    if (pageSize != 20) {
        _url.searchParams.set('pageSize', pageSize);
    }

    if (pageNumber != 1) {
        _url.searchParams.set('page', pageNumber);
    }

    window.location.href = _url.toString();
});
