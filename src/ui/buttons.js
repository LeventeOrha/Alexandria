// Shortcutting the API
const python = new Python()

// Get available shelves and categories
const shelfOptions = python.getShelves()
const categoryOptions = python.getCategories()

// All specific button functions

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

// Change active book
function fillBookData(book) {
    // Select the element to be filled
    let div = document.querySelector(".bookData")

    // Set the id
    div.id = book["ID"]

    // Get all details of the book
    book = python.searchByID(book["ID"])

    // Create the sub elements one by one
    let bookInfo = document.createElement("div")
    bookInfo.className = "bookInfo"

    let details = document.createElement("div")
    details.className ="details"

    let bookHeader = document.createElement("div")
    bookHeader.classList.add("bookHeader")
    bookHeader.classList.add("glass")
    bookHeader.innerHTML = `<div><h1>${book["title"]}</h1><h2>${book["author"]}</h2></div>`

    // Edit and delete buttons
    const buttons = document.createElement("div")
    buttons.className = "editButtonHolder"

    // Edit button
    const editbtn = document.createElement("button")
    editbtn.id = "editBookDetails"
    editbtn.textContent = "Edit"
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
    
    buttons.appendChild(editbtn)

    // TODO - delete button
    const deletebtn = document.createElement("button")
    deletebtn.id = "deleteBook"
    deletebtn.textContent = "Delete"
    deletebtn.addEventListener("click", () => {
        python.deleteBook(book)
        div.replaceChildren() // Clear out the book details
        document.querySelector(`.bookList#${CSS.escape(book["ID"])}`).remove() // Remove it from the results
    })

    buttons.appendChild(deletebtn)

    bookHeader.appendChild(buttons)

    details.appendChild(bookHeader)

    // Category tags
    let pc = document.createElement("p")
    pc.classname = "tagHolder"
    pc.id = "categoryTags"
    pc.textContent = "Categories: "

    book["category"].forEach((category) => {
        let span = document.createElement("span")
        span.className = "tag"
        span.innerHTML = `<span>${category}</span>`
        pc.appendChild(span)
    })

    details.appendChild(pc)

    // Shelf tags
    let ps = document.createElement("p")
    ps.classname = "tagHolder"
    ps.id = "shelfTags"
    ps.textContent = "Shelves: "

    book["shelf"].forEach((shelf) => {
        let span = document.createElement("span")
        span.className = "tag"
        span.innerHTML = `<span>${shelf}</span>`
        ps.appendChild(span)
    })

    details.appendChild(ps)

    // Start date
    let start = document.createElement("p")
    start.id = "start"
    start.textContent = `Start: ${book["start"]}`

    details.appendChild(start)

    // End date
    let end = document.createElement("p")
    end.id = "end"
    end.textContent = `End: ${book["end"]}`

    details.appendChild(end)

    bookInfo.appendChild(details)

    // Image
    let img = document.createElement("img")
    img.src = book["img"]
    bookInfo.appendChild(img)

    div.appendChild(bookInfo)

    // Abstract
    let abst = document.createElement("div")
    abst.className = "abstract"
    abst.innerHTML = book["abstract"]

    div.appendChild(abst)
}

// Do a search IN
function searchIn() {
    // Get key and value to search
    const searchKey = document.getElementById("searchKey").value
    const searchValue = document.getElementById("searchValue").value

    // Perform search in database
    const books = python.searchIn(searchKey, searchValue)

    // Clear out the searchResults div
    const searchResults = document.querySelector(".searchResults")
    searchResults.replaceChildren()

    // Clear out bookData at a new search
    document.querySelector(".bookData").replaceChildren()

    // Add the search results
    books.forEach(book => {
        const div = document.createElement("div")
        div.className = "bookList"
        div.id = book["ID"]

        const img = document.createElement("img")
        img.src = book["img"]
        div.appendChild(img)

        const title = document.createElement("div")
        title.className = "titleAuthor"
        title.innerHTML = `<h1>${book["title"]}</h1>\n<h2>${book["author"]}</h2>`
        div.appendChild(title)

        div.addEventListener("click", function () {
            // Remove the other "current"
            document.querySelector(".bookList.current")?.classList.remove("current")

            // Add "current" to this's class list
            this.classList.add("current")

            // Clear out bookData
            document.querySelector(".bookData").replaceChildren()

            // Fill the book's data out
            fillBookData(book)
        })

        searchResults.appendChild(div)
    })
}

document.getElementById("startSearch").addEventListener("click", searchIn)