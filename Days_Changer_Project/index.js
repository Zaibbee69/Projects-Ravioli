// This will be my event handler
document.getElementById("button-handler").onclick = function()
{
    // Get the value of the input tag
    let dayNumber = Number(document.getElementById("day-number").value);
    let dayHead = document.getElementById("day-head");
    let quoteText = document.getElementById("quote-text");
    let quoteHead = document.getElementById("quote-head");

    // Setting up some variables for ASS-THETICS
    let backgroundImage = "";
    let headBackgroundColor = "";
    let headBorderColor = "";
    let headTextColor = "";
    
    // Now making conditions
    switch(dayNumber)
    {
        case 1:
            dayHead.textContent = "Monday";
            quoteText.textContent = "+--Seek to be Whole, Not Perfect--+";
            backgroundImage = "url(Pics/Monday.jpg)";
            headBackgroundColor = "white";
            headBorderColor = "#B3B4D0";
            headTextColor = "#B3B4D0";
            break;
        case 2:
            dayHead.textContent = "Tuesday";
            quoteText.textContent = "+--Our Love is like the Wind, We can't see it but we can feel it everywhere--+";
            backgroundImage = "url(Pics/Tuesday.webp)";
            headBackgroundColor = "#FAF5C7";
            headBorderColor = "#39C4EB";
            headTextColor = "#39C4EB";
            break;
        case 3:
            dayHead.textContent = "Wednesday";
            quoteText.textContent = "+--The earth has music for those who listen--+";
            backgroundImage = "url(Pics/Wednesday.webp)";
            headBackgroundColor = "#FEFEFE";
            headBorderColor = "#0CA884";
            headTextColor = "#0CA884";
            break;
        case 4:
            dayHead.textContent = "Thursday";
            quoteText.textContent = "+--Love is composed of a single soul inhabiting two bodies--+";
            backgroundImage = "url(Pics/Thursday.webp)";
            headBackgroundColor = "#FCEDC9";
            headBorderColor = "#6EC1C9";
            headTextColor = "#6EC1C9";
            break;
        case 5:
            dayHead.textContent = "Friday";
            quoteText.textContent = "+--I was never insane except upon occasions when my heart was touched--+";
            backgroundImage = "url(Pics/Friday.jpg)";
            headBackgroundColor = "#EDD7CA";
            headBorderColor = "#FD142B";
            headTextColor = "#FD142B";
            break;
        case 6:
            dayHead.textContent = "Saturday";
            quoteText.textContent = "+--Every man dies. Not every man really lives--+";
            backgroundImage = "url(Pics/Saturday.webp)";
            headBackgroundColor = "white";
            headBorderColor = "black";
            headTextColor = "black";
            break;
        case 7:
            dayHead.textContent = "Sunday";
            quoteText.textContent = "+--The slave says to the mighty king: <Your'e Just A Man>";
            backgroundImage = "url(Pics/Sunday.jpg)";
            headBackgroundColor = "white";
            headBorderColor = "#FF0200";
            headTextColor = "#FF0200";
            break;
        default:
            dayHead.textContent = "Day Doesn't Exist";
            quoteText.textContent = "+--No Quote for you, HEHEH--+";
    }

    // Now Setting the appropriate assthetics
    document.body.style.backgroundImage = backgroundImage;
    dayHead.style.backgroundColor = headBackgroundColor;
    dayHead.style.border = `6px solid ${headBorderColor}`;  
    dayHead.style.color = headTextColor;
    quoteHead.textContent = "Quote Of The Day";
};
