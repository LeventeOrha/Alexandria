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

const propertySelect = document.querySelector('select[id="searchKey"]');

propertySelect.addEventListener("change", updateSearchField);

// Run once on page load
updateSearchField();

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
