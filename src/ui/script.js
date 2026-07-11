// Part to move have the navigation panel and the moving indicator on it
const navButtons = document.querySelectorAll('nav button');
const indicator = document.querySelector('.indicator');
const mainDivs = document.querySelectorAll(".main")

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

// Initial position
moveIndicator(document.querySelector('.active'));

const propertySelect = document.querySelector('select[id="searchKey"]');

propertySelect.addEventListener("change", updateSearchField);

// Run once on page load
updateSearchField();

// Function to fill out the search part to be a select/option at category/shelf
function updateSearchField() {
    const oldField = document.getElementById("searchValue");

    let newField;

    if (propertySelect.value === "shelf") {
        newField = document.createElement("select");
        newField.id = "searchValue";
        newField.className = "glass";

        shelfOptions.forEach(value => {
            const option = document.createElement("option");
            option.value = value;
            option.textContent = value;
            newField.appendChild(option);
        });

    } else if (propertySelect.value === "category") {
        newField = document.createElement("select");
        newField.id = "searchValue";
        newField.className = "glass";

        for (const key of Object.keys(categoryOptions)) {
            const option = document.createElement("option");
            option.value = key;
            option.textContent = categoryOptions[key];
            newField.appendChild(option);
        } 

    } else {
        newField = document.createElement("input");
        newField.type = "text";
        newField.id = "searchValue";
        newField.className = "glass";
    }

    oldField.replaceWith(newField);
}

// Set the distance from the left edge of main divs on startup
const navHolder = document.querySelector(".nav-holder");

function positionMain() {
    const navWidth = navHolder.getBoundingClientRect().width;
    const vw = window.innerWidth * 0.015; // 1.5vw in pixels

    const left = navWidth + vw;

    mainDivs.forEach(div => {
        div.style.left = `${left}px`;
    });
}

positionMain();
// And at every resize
window.addEventListener("resize", positionMain);