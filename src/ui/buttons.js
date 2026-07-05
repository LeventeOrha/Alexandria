// All specific button functions

// Get shelves and categories
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

// Edit and save mode for a book's details
const editbtn = document.getElementById("editBookDetails")

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

// Edit mode
function editBook() {
    // Add the remove button to each tag
    const tags = document.querySelectorAll(".tag")
    tags.forEach(tag => {
        const removebtn = document.createElement("button")
        removebtn.textContent = "-"
        removebtn.className = "removeTag"

        removebtn.addEventListener("click", () => {
            tag.remove()
        })

        tag.appendChild(removebtn)
    })

    // Add the add category button
    const addCategory = document.createElement("button")
    addCategory.textContent = "+"
    addCategory.className = "addTag"
    addCategory.id = "addCategory"
    addCategory.addEventListener("click", () => {
        insertSelect("addCategory", categoryOptions);
    })

    document.getElementById("categoryTags").appendChild(addCategory)

    // Add the add shelf button
    const addShelf = document.createElement("button")
    addShelf.textContent = "+"
    addShelf.className = "addTag"
    addShelf.id = "addShelf"
    addShelf.addEventListener("click", () => {
        insertSelect("addShelf", shelfOptions);
    })

    document.getElementById("shelfTags").appendChild(addShelf)

    // Change start to input
    const startDate = document.getElementById("start")
    // TODO - change it here to actual date parsing and not this "quick" solution
    let date = startDate.textContent.split(" ")[1]
    startDate.innerHTML = `Start: <input type="date" value="${date}" class="dateTag">`

    // Change end to input
    const endDate = document.getElementById("end")
    date = endDate.textContent.split(" ")[1]
    if (date == "---"){
        endDate.innerHTML = `End: <input type="date" class="dateTag">`
    }
    else {
        endDate.innerHTML = `End: <input type="date" value="${date}" class="dateTag">`
    }
}

// Save mode
function saveBook() {

}

// Toggle save and edit
editbtn.addEventListener("click", () => {
    if (editbtn.textContent == "Edit") {
        editBook()
        editbtn.textContent = "Save"
    }
    else {
        saveBook()
        editbtn.textContent = "Edit"
    }
})