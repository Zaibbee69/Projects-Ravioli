// Adding my button to change theme of my whole website

// Waiting for DOM content to be loaded
document.addEventListener("DOMContentLoaded", () => {

    // Selecting the button first
    document.getElementById("change-theme").onclick = changeTheme;

    // Assigning Icons to the span
    const iconElements = document.querySelectorAll(".random-icon");

    // Assign a random icon
    iconElements.forEach(iconElement => {
        iconElement.textContent = getRandomIcon();
    })

    // Adding a listener for if user wants to edit a post
    document.querySelectorAll(".edit-button").forEach(button => {

        // When user clicks on the button
        button.onclick= () => editPost(button);
    })

    // Adding a listener for when user likes a post
    document.querySelectorAll(".like-button").forEach(button => {

        // When the user clicks on the button
        button.onclick= () => likePost(button);
    })

    // Now making my function for following a user
    const followBtn = document.querySelector(".follow-button")
    
        followBtn.onclick = () => {

        // Getting the name for the user who to follow
        const userName = followBtn.dataset.userNamed;
        
        // Now making the fetch request to api
        fetch(`/profile/${userName}/follow`, {
            method: "POST"
        })

        // Now getting the returned data and turning to JSON
        .then(response => response.json())

        // Now manipulating the data
        .then(data => {

            // Checking for errors
            if (data.error)
            {
                console.error(data.error);
            }

            else
            {
                // Getting the followers and following
                const followers_count = document.getElementById("follower-count");

                // Update the followers count on the page
                followers_count.textContent = `Followers: ${data.followers_count}`;

                // Now updating the datas
                if (data.follow_status)
                {
                    followBtn.textContent = "Unfollow";
                }
                else
                {
                    followBtn.textContent = "Follow";
                }
            }
        })
        // Catching any errors
        .catch(error => console.error("Error:", error));
    }
});


// Function for liking posts
function likePost(button)
{

    // Getting the id of the post
    const postId = button.dataset.postId;

    // Now sending the data to API
    fetch(`post/${postId}/like`, {
        method: "POST"
    })

    // Now getting the returned response and turning to JSON
    .then(response => response.json())

    // Now manipulating that data
    .then(data => {

        // If given error
        if (data.error)
        {
            console.error(data.error)
        }

        else
        {
            // Updating the like count and button text
            const likeCount = document.getElementById(`like-count-${postId}`);

            // Now updating it to likes count
            likeCount.textContent = `Likes: ${data.like_count}`;

            // Now updating the text count
            if (data.liked)
            {
                button.textContent = "Unlike";
            }
            else
            {
                button.textContent = "Like";
            }
        }
    })

    // Catching any errors
    .catch(error => console.error("Error:", error));
}
// Function for editing posts
function editPost(button)
{
    // First i will be getting the posts id from the button dataset
    const postId = button.dataset.postId;
            
    // Getting the div where the posts resides
    const postDiv = document.getElementById(`post-${postId}`);
    
    // Selecting the content within that specific Div
    const postContent = postDiv.querySelector(".post-content");
    
    // Creating a new text area
    const textArea = document.createElement("textarea");

    // Populating it with existing data
    textArea.value = postContent.textContent;
    postContent.replaceWith(textArea);

    // Now also chaning the button to display save
    button.textContent = "Save";

    // Now saving the content process
    button.onclick = () => savePost(button, textArea, postId);
}


// Function for saving posts
function savePost(button, textArea, postId)
{
    // Getting the updated content 
    const updatedContent = textArea.value;

    // Now sending request to server
    fetch(`/post/${postId}/edit`, {
        method: "POST",
        body: new URLSearchParams({
            "content": updatedContent
        })
    })

    // Now taking the data and turning it into json
    .then(response => response.json())

    // Now manipulating data
    .then(data => {

        // If data had an error
        if(data.error)
        {
            console.error(data.error);
        }

        // Otherwise updating my post
        else
        {
            // I will create a new paragraph element
            const updateData = document.createElement("p");

            // Giving it a class
            updateData.className = "post-content";

            // And assigning its new content
            updateData.textContent = updatedContent;

            // Now just putting the data in post
            textArea.replaceWith(updateData);

            // Also changing the button back
            button.textContent = "Edit";
        }
    })
    // Catching errors
    .catch(error => console.error("Error:", error));
}


// Function to change the theme of my website
function changeTheme() {
    
    // Getting the body of the HTML
    const body = document.body;

    // Making check for themes bow
    if (body.classList.contains("dark-theme"))
    {
        body.classList.remove("dark-theme");
        body.classList.add("light-theme");
    }
    else
    {
        body.classList.remove("light-theme");
        body.classList.add("dark-theme");
    }
}


// My function which gives me completely different icons everytime

    // My ICONS
    const icons = [
        "star",
        "favorite",
        "star_half",
        "change_circle",
        "cloud",
        "borg",
        "pets",
        "rocket",
        "cruelty_free",
        "bedtime",
        "raven"
    ];

    function getRandomIcon() {
        return icons[Math.floor(Math.random() * icons.length)]
    }