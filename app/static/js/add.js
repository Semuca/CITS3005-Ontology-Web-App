const tabContainer = document.getElementById("add-tabs");

const addButton = document.getElementById("addButton");

const tabIdToRequiredFields = {
	"add-procedure-tab": ["searchInput"],
	"add-part-tab": ["searchInput"],
	"add-item-tab": ["searchInput"],
	"add-tool-tab": ["searchInput"],
};

function setupValidation() {
	for (const tabId in tabIdToRequiredFields) {
		const tabWindow = tabContainer.querySelector(`#${tabId}`);

		const requiredFields = tabIdToRequiredFields[tabId];

		for (const field of requiredFields) {
			tabWindow
				.querySelector(`#${field}`)
				.addEventListener("input", validateAddButton);
		}
	}

	validateAddButton();
}

function validateAddButton() {
	const selectedTabWindow = tabContainer.querySelector(".tab-content.active");

	const requiredFields = tabIdToRequiredFields[selectedTabWindow.id];

	for (const field of requiredFields) {
		if (!selectedTabWindow.querySelector(`#${field}`).value) {
			addButton.disabled = true;
			return;
		}
	}

	addButton.disabled = false;
}

setupValidation();

addButton.addEventListener("click", () => {
	const selectedTabWindow = tabContainer.querySelector(".tab-content.active");
	const rdf_type = selectedTabWindow.getAttribute("data-rdf-type");

	const propertyInputs =
		selectedTabWindow.querySelectorAll(".property-input");
	const properties = {};

	propertyInputs.forEach((input) => {
		const property = input.getAttribute("data-property");
		const value = input.value;
		if (value) {
			properties[property] = value;
		}
	});

	fetch("/api/", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({
			rdf_type: rdf_type,
			properties: properties,
		}),
	})
		.then((response) => {
			if (!response.ok) {
				throw new Error(response.statusText);
			}
			return response.text();
		})
		.then((data) => {
			location.reload();
		})
		.catch((error) => {
			console.error(error);
		});
});
