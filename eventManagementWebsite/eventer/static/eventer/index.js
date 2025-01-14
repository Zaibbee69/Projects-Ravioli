// Function to toggle the description of an event

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById('newsletter-form').addEventListener('submit', function(event) {
        event.preventDefault();  // Prevent the default form submission
    
        // Get the form element and prepare the data
        const form = event.target;
        const formData = new FormData(form);
    
        // Get the CSRF token value
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
        // Send the AJAX request
        fetch(form.action, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken  // Include the CSRF token in the headers
            },
            body: formData
        })
        .then(response => response.json())  // Expect JSON response
        .then(data => {
            // Display the response messages
            const messageContainer = document.getElementById('message-container');
            messageContainer.innerHTML = data.message;  // Insert the HTML message content
    
            // Clear the email input on success
            if (data.message.includes('success')) {
                form.reset();
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
})

function toggleDescription(element){

    // Find the parent container
    var eventContainer = element.closest(".event-item, .upcoming-events-item ");

    // Getting the element which was clicked
    var truncated = eventContainer.querySelector(".event-item-description, .upcoming-event-description");
    var full = eventContainer.querySelector(".event-item-description-full, .upcoming-event-description-full");

    // Checking wether to display description or not
    if (full.style.display === "none")
    {
        truncated.style.display = "none";
        full.style.display = "block";
    }
    else
    {
        truncated.style.display = "block";
        full.style.display = "none";
    }
}