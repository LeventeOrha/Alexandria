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

const propertySelect = document.querySelector('select[name="property"]');

propertySelect.addEventListener("change", updateSearchField);

// Run once on page load
updateSearchField();

function updateSearchField() {
    const oldField = document.getElementById("searchValue");

    let newField;

    if (propertySelect.value === "shelf" || propertySelect.value === "category") {
        newField = document.createElement("select");
        newField.id = "searchValue";
        newField.className = "glass";

        const options = propertySelect.value === "shelf"
            ? shelfOptions
            : categoryOptions;

        options.forEach(value => {
            const option = document.createElement("option");
            option.value = value;
            option.textContent = value;
            newField.appendChild(option);
        });

    } else {
        newField = document.createElement("input");
        newField.type = "text";
        newField.id = "searchValue";
        newField.className = "glass";
    }

    oldField.replaceWith(newField);
}
