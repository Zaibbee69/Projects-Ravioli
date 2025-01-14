// Waiting for DOM content to be loaded
document.addEventListener("DOMContentLoaded", () => {

    // Selecting modal buttons for closing it earlier
    var closeModal = document.querySelector(".event-modal-closer");

    // Making it so that when it is clicked
    closeModal.onclick = modalCloserInside;

    // Also making so that if user clicks outside the modal also close it then
    window.onclick = modalCloserOutside;

    // Selecting the div for inputting
    var calendarEl = document.getElementById("calendar");

    // Making that div into a calender
    var calendar = new FullCalendar.Calendar(calendarEl, {

        // Setting the calendar format
        initialView: "dayGridMonth",

        // The api request of the url
        events: "/events/feeds/",
     
        eventColor: 'cornflowerblue',

        eventBorderColor: "#1B263B",

        eventTextColor: "white",

        // Setting what will happen when an event will be clicked
        eventClick: function(info) {

            // First populating all the divs with 
            document.getElementById("event-modal-title-entry").textContent = info.event.title;
            document.getElementById("event-modal-date-entry").textContent = info.event.start.toDateString();
            document.getElementById("event-modal-description-entry").textContent = info.event.extendedProps.description || "No Description available";
            document.getElementById("event-modal-location-entry").textContent = info.event.extendedProps.location || "No Location available";

            // Now showing the modal
            document.getElementById("eventModal").style.display = "block";
        }
    });
    // Now rendering my calender
    calendar.render()
});


// Function for when user clicks oustide the modal
function modalCloserOutside(event)
{
    var modal = document.getElementById("eventModal");

    // Checker where the user clicked
    if (event.target == modal){
        modal.style.display = "none";
    }
}


// Function when user clicks inside the modal
function modalCloserInside()
{
    document.getElementById("eventModal").style.display = "none";
}