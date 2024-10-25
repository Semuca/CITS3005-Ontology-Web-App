const addLinkButtons = document.getElementsByClassName("addLinkButton");

for (let addLinkButton of addLinkButtons) {
	addLinkButton.addEventListener("click", (event) => {
		const parentDiv = event.target.closest("div");
		const parentUri = parentDiv.getAttribute("parent-uri");
		const childUri = parentDiv.getAttribute("child-uri");
		const linkProperty = parentDiv.getAttribute("data-property");
		const objectType = parentDiv.getAttribute("data-object-type");
		const inputField = parentDiv.querySelector("#idInput");
		const inputtedId = inputField.value;

		console.log(parentUri, childUri, linkProperty, objectType, inputtedId);

		fetch("/api/links", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({
				parentUri: parentUri,
				childUri: childUri,
				property: linkProperty,
				linkId: inputtedId,
				objectType: objectType,
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
}
