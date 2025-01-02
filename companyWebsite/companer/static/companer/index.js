// Dom loading
document.addEventListener("DOMContentLoaded", () => {
        const contactSection = document.getElementById('contact-section');
        const whySection = document.getElementById('why-section');
        const contactContent = document.getElementById('contact-content');
        const whyContent = document.getElementById('why-content');

        contactSection.addEventListener('click', function() {
            hideBothSections();
            contactContent.classList.add('active');
        });

        whySection.addEventListener('click', function() {
            hideBothSections();
            whyContent.classList.add('active');
        });

        function hideBothSections() {
            document.querySelector('.container').style.display = 'none';
        }

        function showBothSections() {
            document.querySelector('.container').style.display = 'flex';
            contactContent.classList.remove('active');
            whyContent.classList.remove('active');
        }
})

// Function to change the search bar
function toggleSearch() {

    // Selecting the search bar
    const searchBar = document.querySelector(".search-bar-container");

    // Making it display block
    searchBar.style.display = searchBar.style.display === 'block' ? 'none' : 'block';
}

