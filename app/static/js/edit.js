const editableParagraphs = document.querySelectorAll(
	'p[contenteditable="true"]'
);

for (let editableParagraph of editableParagraphs) {
	editableParagraph.addEventListener("input", () => {
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
	});
}
