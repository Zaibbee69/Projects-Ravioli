document.addEventListener("DOMContentLoaded", ()=> {

    // Typing Effect for Hero Section
    const typingText = "DevOps: Automating Collaboration & Innovation";
    let index = 0;

    function typeEffect() {
        const span = document.querySelector(".typing");
        if (index < typingText.length) {
            span.textContent += typingText[index];
            index++;
            setTimeout(typeEffect, 20);
        }
    }

    window.addEventListener("load", typeEffect);

    // Show DevOps Fun Fact
    const showFactBtn = document.getElementById("showFact");
    const fact = document.getElementById("fact");

    showFactBtn.addEventListener("click", () => {
        fact.style.display = fact.style.display === "none" ? "block" : "none";
    });

})

function checkAnswers() {
    const answers = {
        q1: 'a',
        q2: 'a',
        q3: 'a',
        q4: 'a'
    };

    let score = 0;
    for (let question in answers) {
        const selected = document.querySelector(`input[name="${question}"]:checked`);
        if (selected && selected.value === answers[question]) {
            score++;
        }
    }

    document.getElementById('score').innerText = score;
    document.getElementById('resultMessage').style.display = 'block';
}