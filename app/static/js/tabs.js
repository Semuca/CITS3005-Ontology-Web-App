function openTab(event, tabContainer, tabName) {
    // Get tab container
    const container = document.getElementById(tabContainer);

    // Hide all tab content
    const tabContents = container.querySelectorAll('.tab-content');
    tabContents.forEach(content => {
        content.classList.remove('active');
    });

    // Remove active class from all tab buttons
    const tabButtons = document.querySelectorAll('.tab-button');
    tabButtons.forEach(button => {
        button.classList.remove('active');
    });

    // Show the selected tab content and add active class to the button
    document.getElementById(tabName).classList.add('active');
    event.currentTarget.classList.add('active');
}