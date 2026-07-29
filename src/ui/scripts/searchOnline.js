// Do an online search
const startOnlineSearch = document.getElementById("startOnlineSearch")
startOnlineSearch.addEventListener("click", async () => {
    document.body.style.cursor = "wait"
    const title = document.getElementById("onlineTitle").value
    const author = document.getElementById("onlineAuthor").value
    console.log(`Search started with title: ${title} & author: ${author}.`)

    // Get the language to search
    const lang = document.getElementById("language").value

    // Perform the online search
    const books = await window.python.searchOut(title, author, lang)

    // Get the placeholder to put the results in
    const results = document.getElementById("onlineResults")

    // Put in a "No result found" message if there are no results
    if (books === null) {
        console.log("No results.")
        const h1 = document.createElement("h1")
        h1.textContent = window.app.inCodeText["NoSearchResults"]
        results.appendChild(h1)
        document.body.style.cursor = "default"
        return
    }

    // Clear out earlier results
    results.replaceChildren()

    // Put each book out
    books.forEach((book) => {
        const div = document.createElement("div")
        div.classList.add("onlineResult")
        div.classList.add("glass")
        div.id = book["ID"]
        div.dataset.img = book["img"]

        const check = document.createElement("input")
        check.type = "checkbox"
        check.className = "pickBook"
        div.appendChild(check)

        const img = document.createElement("img")
        img.src = book['img']
        div.appendChild(img)

        const h1 = document.createElement("h1")
        h1.textContent = book["title"]
        div.appendChild(h1)

        const h2 = document.createElement("h2")
        h2.textContent = book["author"]
        div.appendChild(h2)

        const span = document.createElement("span")
        span.textContent = book["date"]
        div.appendChild(span)

        results.appendChild(div)
    })
    console.log("Search finished.")
    document.body.style.cursor = "default"
})

// On page load, place in all available shelves in this select/option
const saveShelf = document.getElementById("saveShelf")
window.app.shelfOptions.forEach((shelf) => {
    const option = document.createElement("option")
    option.value = shelf
    option.textContent = shelf
    saveShelf.appendChild(option)
})

// Save new books on a shelf button
document.getElementById("saveBooksOnShelf").addEventListener("click", async () => {
    const shelf = document.getElementById("saveShelf").value
    var ids = []
    var imgs = []
    document.querySelectorAll(".pickBook").forEach(checkbox => {
        if (checkbox.checked) {
            ids.push(checkbox.closest("div").id)
            imgs.push(checkbox.closest("div").dataset.img)
        }
    })
    await window.python.addBooks(ids, shelf, imgs)
    console.log("Save successful!")
})