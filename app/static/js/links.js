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

const deleteLinkButtons = document.getElementsByClassName("deleteLinkButton");

for (let deleteLinkButton of deleteLinkButtons) {
	deleteLinkButton.addEventListener("click", (event) => {
		event.stopPropagation();
		event.preventDefault(); // Prevent the default action (following the link)

		let parentUri = event.target.getAttribute("parent-uri");
		let childUri = event.target.getAttribute("child-uri");
		const uri = event.target.getAttribute("data-uri");
		const linkProperty = event.target.getAttribute("data-property");

		if (parentUri === "None") parentUri = null;
		if (childUri === "None") childUri = null;

		fetch("/api/links", {
			method: "DELETE",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({
				parentUri: parentUri,
				childUri: childUri,
				uri: uri,
				property: linkProperty,
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
