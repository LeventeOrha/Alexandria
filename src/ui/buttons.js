// Shortcutting the API
const python = new Python()

// Get available shelves and categories
const shelfOptions = python.getShelves()
const categoryOptions = python.getCategories()

// All specific button functions

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
    startDate.innerHTML = `Start: <input type="date" value="${date}" class="dateTag" id="startDate">`

    // Change end to input
    const endDate = document.getElementById("end")
    date = endDate.textContent.split(" ")[1]
    if (date == "---"){
        endDate.innerHTML = `End: <input type="date" class="dateTag" id="endDate">`
    }
    else {
        endDate.innerHTML = `End: <input type="date" value="${date}" class="dateTag" id="endDate">`
    }
}

// Save mode
function saveBook() {
    // Get the book's all data from the database
    let book = python.searchByID(document.querySelector(".bookData").id)

    // Remove "removeTag" buttons
    let removes = document.querySelectorAll(".removeTag")
    removes.forEach((element) => {element.remove()})

    // Remove "addTag" buttons
    removes = document.querySelectorAll(".addTag")
    removes.forEach((element) => {element.remove()})

    // And now update the fields
    // First the categories
    let categories = document.getElementById("categoryTags")
    categories = [...categories.querySelectorAll(".tag")].map(el =>
        el.matches("span") ? el.textContent.trim() : el.value
    )
    book["category"] = categories

    // Now the shelves
    let shelf = document.getElementById("shelfTags")
    shelf = [...shelf.querySelectorAll(".tag")].map(el =>
        el.matches("span") ? el.textContent.trim() : el.value
    )
    book["shelf"] = shelf

    // Starting date
    book["start"] = document.getElementById("startDate").value

    // End date
    book["end"] = document.getElementById("endDate").value

    // Save the updated book
    python.saveBook(book)

    console.log(book)

    // Replace existing select/options with its value
    let selects = document.querySelectorAll("select.tag")
    selects.forEach((select) => {
        const tag = document.createElement("span")
        tag.className = "tag"

        tag.innerHTML = `<span>${select.options[select.selectedIndex].text}</span>`

        select.replaceWith(tag)
    })

    // Replace all date inputs with the values
    document.querySelectorAll('input.dateTag[type="date"]').forEach(input => {
        const span = document.createElement('span');
        span.textContent = input.value || '---';
        input.replaceWith(span);
    });

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