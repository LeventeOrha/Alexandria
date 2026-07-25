// Navigation bar functions
// Part to move have the navigation panel and the moving indicator on it
const navButtons = document.querySelectorAll('nav button')
const indicator = document.querySelector('.indicator')

function moveIndicator(button) {
    indicator.style.top = button.offsetTop + 'px';
}

navButtons.forEach((button, index) => {
    button.addEventListener("click", () => {
        moveIndicator(button);

        mainDivs.forEach((div, divIndex) => {
            // Reset classes first
            div.classList.remove("lower", "higher");

            if (divIndex < index) {
                div.classList.add("higher");
            } else if (divIndex > index) {
                div.classList.add("lower");
            }
        });
    });
});

// If this is a new user, force them onto the settings page
if (python.isNewUser()) {
    document.getElementById("homeButton").classList.remove("active")
    document.getElementById("settingsButton").classList.add("active")
}

// Initial position
moveIndicator(document.querySelector('.active'));