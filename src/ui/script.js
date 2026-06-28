// Part to move have the navigation panel and the moving indicator on it
const navButtons = document.querySelectorAll('nav button');
const indicator = document.querySelector('.indicator');

function moveIndicator(button) {
    indicator.style.top = button.offsetTop + 'px';
}

navButtons.forEach(button => {
    button.addEventListener('click', () => {
        moveIndicator(button);
    });
});

// Initial position
moveIndicator(document.querySelector('.active'));