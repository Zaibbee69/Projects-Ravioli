// Ok first making sure the whole file has loaded

document.addEventListener("DOMContentLoaded" , function()
{
    // For the gaming table

    let batman = document.getElementById("gam-fav-button"); // Getting the element by ID
    batman.addEventListener("click" , batman_func); // Listening for input

    // Batman function

    function batman_func()
    {
        let batman_img = document.getElementById("batman-img");
        batman_img.src = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRoqYPhliQYPr4MeYFn3RzSWXqi7b7dDMseKA&usqp=CAU";
        batman_img.classList.add("rotating");
        setTimeout(function()
        {
            batman_img.src="";
            batman_img.classList.remove("rotating");
        } , 4000);
    }

    // For the cats table

    let cats_pic = document.getElementById("cats-vidpic"); // Getting the element by ID
    cats_pic.addEventListener("click" , cats_func); // Listening for input

    // Cats function

    function cats_func()
    {
        cats_pic.remove();
    }

    // For the Musics table

    let random_button = document.getElementById("music-button");
    random_button.addEventListener("click" , link_func);

    // Link function

    function link_func (event)
    {
        let urls = ["https://open.spotify.com/embed/track/3ZaEs1O8BG581qYPHpQ8d6?utm_source=generator"
         , "https://open.spotify.com/embed/track/4dSEKivGPiEAX5pwcemIXL?utm_source=generator" ,
        "https://open.spotify.com/embed/track/0RBw4ODUQPO4cuAOZtBGga?utm_source=generator"
        , "https://open.spotify.com/embed/track/2K70ZV0Ls65Kkj0WUEfHlz?utm_source=generator"];
        let randomUrl = urls[Math.floor(Math.random() * urls.length)];
        let random_a = document.getElementById("music-a");
        random_a.href = randomUrl;
    }

    // For the Anime table

    let shari = document.getElementById("anime-button");
    shari.addEventListener("click" , shari_func);

    function shari_func()
    {
        let pic = document.getElementById("sharinggan");
        shari.style.display = "none";

        pic.src = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQlQFVooQb9xqsbzIPyCVCDfh7_3-VX2VHbKA&usqp=CAU";

        setTimeout( sharingan , 3000);

        function sharingan ()
        {
            shari.style.display = "block";
            pic.src = ""
        }
    }
})
