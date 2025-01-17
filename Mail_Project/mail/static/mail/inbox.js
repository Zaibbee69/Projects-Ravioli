document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  // Making my function for taking the data the user sents through a form to my database in python route

  // First i will be getting the form 
  document.querySelector("#compose-form").onsubmit = (event) => {
    event.preventDefault();

    // Now getting all the values from the form
    const recipients = document.querySelector("#compose-recipients").value;
    const subject = document.querySelector("#compose-subject").value;
    const body = document.querySelector("#compose-body").value;

    // Now im gonna send the data to my API aka view
    fetch("/emails", {
      method: "POST",
      body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
      })
    }) 

    // Converting my data to json format
    .then(response => response.json())

    // Now logging info and redirecting user to sent tab
    .then(result => {
      console.log(result);

      // Checking if email was sent correctly
      if (result.message === "Email sent successfully.")
      {
        // Load the email inbox
        load_mailbox("sent");
      }
      else
      {
        console.error(result.error);
      }
    });
  };
});


function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector("#email-view").style.display = "none";
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}


function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector("#email-view").style.display = "none";
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  const emailView = document.querySelector('#emails-view');
  emailView.innerHTML = `<h3 class="mail-header">${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3><hr>`;

  // Making a function to load the emails when user visits any kind of mailbox
  fetch(`/emails/${mailbox}`)
  
  // Converting the server response to JSON
  .then(response => response.json())
  
  // Now handling the data
  .then(emails => {
  
    // Now imma be displaying each email one by one
    emails.forEach(email => {
    
      // Creating each element as a div
      const emailDiv = document.createElement("div");
    
      // Giving each email a class
      emailDiv.className = "email-component";
    
      // Now entering data in the div
      emailDiv.innerHTML = `<strong class="name-status">${email.sender}</strong> ||  
                            <span>${email.subject}</span> ||
                            <span>${email.timestamp}</span> ||
                            <span class="read-status">${email.read ? 'Read' : 'Unread'}</span>||`;

      // Checking logic if the email was read or not
      if (!email.read) {
        emailDiv.style.backgroundColor = "white";
      } else {
        emailDiv.style.backgroundColor = "whitesmoke";
      }

      // Now I will be checking whether the email was in inbox or archived position
      if (mailbox === "inbox") {
        emailDiv.innerHTML += ` <button class="archive-button">Archive</button>`;

        // Now I will be checking whether the button was pressed or not
        emailDiv.querySelector(".archive-button").addEventListener("click", (event) => {
          event.stopPropagation();  // Prevent the event from triggering the email view

          // Adding animations
          emailDiv.classList.add("smoo-ther");

          emailDiv.addEventListener("animationend", ()=>{
            archive_email(email.id, true);
            emailDiv.remove();
          });
        });
      } 
      else if (mailbox === "archive") {
        emailDiv.innerHTML += ` <button class="archive-button">Unarchive</button>`;

        // Now I will be checking whether the button was pressed or not
        emailDiv.querySelector(".archive-button").addEventListener("click", (event) => {
          event.stopPropagation();  // Prevent the event from triggering the email view

          // Adding animations
          emailDiv.classList.add("smoo-ther");

          emailDiv.addEventListener("animationend", ()=>{
            archive_email(email.id, false);
            emailDiv.remove();
          });  
        });
      }

      // Adding an event listener if user clicks on any email
      emailDiv.addEventListener("click", () => load_email(email.id)); 

      // Now appending data to the div
      emailView.appendChild(emailDiv);
    
    });
  });
}


// Making a function for displaying individual elements clicked on email
function load_email(email_id){

  // First imma load only the email id and cancel others 
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#email-view").style.display = "block";
  document.querySelector("#compose-view").style.display = "none";

  // Ok so  imma fetch the email data based on id
  fetch(`/emails/${email_id}`)

  // Now convert the returned response the JSON
  .then(response => response.json())

  // Now handling the returned data
  .then(email => {

    // Updating the html to display the data
    document.querySelector("#email-view").innerHTML = `<div><p class="reply-one"><strong class="stronger">From:</strong>${email.sender}</p></div> 
                                                       <div><p class="reply-two"><strong class="stronger">To:</strong>${email.recipients}</p></div>
                                                       <div><p class="reply-one"><strong class="stronger">Subject:</strong>${email.subject}</p></div>
                                                       <div><p class="reply-two"><strong class="stronger">Timestamp:</strong>${email.timestamp}</p></div>
                                                       <button id="reply-button">Reply</button>
                                                       <div class="reply-body"><p>${email.body}</p></div>`;

    // Now i am adding a listener if the button was clicked or not
    document.querySelector('#reply-button').addEventListener('click', () => compose_email_reply(email));

    // Now im gonna update the email to be marked as read
    if (!email.read)
    {
      fetch(`/emails/${email_id}`, {
        method: "PUT",
        body: JSON.stringify({
          read: true
        })
      })
    }
  });
}


// Function for archiving emails
function archive_email(email_id, archive) {

  // Send a PUT request to archive/unarchive the email
  fetch(`/emails/${email_id}`, {
    method: "PUT",
    body: JSON.stringify({
      archived: archive
    })
  })
  .then(() => {

    // Reload the inbox to reflect changes
    load_mailbox('inbox');
  });
}


// Function when someone clicks on the reply button
function compose_email_reply(email){

  // First hiding and showing the correct divs
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#email-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "block";

  // Now i will be prefilling the documents with data as required
  document.querySelector("#compose-recipients").value = email.sender;
  document.querySelector("#compose-subject").value = email.subject.startsWith("Re:") ? email.subject: `Re: ${email.subject}`;
  document.querySelector("#compose-body").value = `On ${email.timestamp} ${email.sender} wrote: \n${email.body}\n\n`;
}