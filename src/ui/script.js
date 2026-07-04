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

// Part to change the list of category and shelf
// TODO - change code here for actual shelves and categories from the database
const shelfOptions = [
    "Reading",
    "Read",
    "To read"
];

const categoryOptions = [
    "Fiction",
    "Science",
    "History",
    "Biography"
];

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

// When editing the shelves and categories, create a select/option before the Add button
function insertSelect(buttonId, options) {
  const button = document.getElementById(buttonId);

  const select = document.createElement("select");

  select.className = "tag"

  options.forEach(optionText => {
    const option = document.createElement("option");
    option.value = optionText;
    option.textContent = optionText;
    select.appendChild(option);
  });

  button.parentNode.insertBefore(select, button);
}

document.getElementById("addShelf").addEventListener("click", () => {
  insertSelect("addShelf", shelfOptions);
});

document.getElementById("addCategory").addEventListener("click", () => {
  insertSelect("addCategory", categoryOptions);
});

// Remove a tag
document.addEventListener("click", (event) => {
    if (event.target.classList.contains("removeTag")) {
        event.target.parentElement.remove();
    }
});