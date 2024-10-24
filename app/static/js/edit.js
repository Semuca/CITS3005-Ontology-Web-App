const editableParagraphs = document.querySelectorAll(
	'p[contenteditable="true"]'
);

// Debounce function
function debounce(func, wait) {
	let timeout;
	return function (...args) {
		const context = this;
		clearTimeout(timeout);
		timeout = setTimeout(() => func.apply(context, args), wait);
	};
}

// Function to handle input event
function handleInput(event) {
	const editableParagraph = event.target;
	const uri = editableParagraph.getAttribute("data-uri");
	const property = editableParagraph.getAttribute("data-property");
	const newValue = editableParagraph.innerText;

	fetch("/api/", {
		method: "PUT",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({
			uri: uri,
			property: property,
			new_value: newValue,
		}),
	})
		.then((response) => {
			if (!response.ok) {
				throw new Error(response.statusText);
			}
			return response.text();
		})
		.then((data) => {
			// console.log(data);
		})
		.catch((error) => {
			console.error(error);
		});
}

// Debounced version of the handleInput function
const debouncedHandleInput = debounce(handleInput, 300);

for (let editableParagraph of editableParagraphs) {
	editableParagraph.addEventListener("input", debouncedHandleInput);
}
