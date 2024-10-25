const openDeleteModalButtons =
	document.getElementsByClassName("openDeleteButton");

let uriToDelete = "";

for (let openDeleteModalButton of openDeleteModalButtons) {
	openDeleteModalButton.addEventListener("click", (event) => {
		uriToDelete = event.target.getAttribute("data-uri");
	});
}

const deleteButton = document.getElementById("deleteButton");

deleteButton.addEventListener("click", () => {
	fetch("/api/", {
		method: "DELETE",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({
			uri: uriToDelete,
		}),
	})
		.then((response) => {
			if (!response.ok) {
				throw new Error(response.statusText);
			}
			return response.text();
		})
		.then((data) => {
			window.location.href = "/";
			location.reload();
		})
		.catch((error) => {
			console.error(error);
		});
});
