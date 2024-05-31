
// ------------------------------------------------------------------------

document.addEventListener("DOMContentLoaded", function() {
    const tabs = document.querySelectorAll('.btn_tab');
    const contents = document.querySelectorAll('.content');

    // Function to remove active states
    function deactivateAllTabs() {
        tabs.forEach(t => {
            t.classList.remove('active_tab'); // Remove active state from all tabs
        });
        contents.forEach(c => {
            c.classList.remove('active'); // Hide all content divs
            c.classList.add('hidden');
        });
    }

    // Set the first tab as active initially
    tabs[0].classList.add('active_tab');
    contents[0].classList.add('active');
    contents[0].classList.remove('hidden');

    // Add click event listeners to tabs
    tabs.forEach((tab, index) => {
        tab.addEventListener('click', function() {
            deactivateAllTabs(); // Deactivate all tabs and hide their contents
            tab.classList.add('active_tab'); // Activate the clicked tab
            contents[index].classList.add('active'); // Show the corresponding content
            contents[index].classList.remove('hidden');
        });
    });
});

