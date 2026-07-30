// Fill out the carousel at currentReading
async function fillCurrentReading(shelf) {
    const books = await window.python.searchIn("shelf", shelf)

    const carousel = document.getElementById("currentBody")
    carousel.replaceChildren() // Empty it out
    books.forEach(book => {
        const slide = document.createElement("div")
        slide.className = "slide"

        const img = document.createElement("img")
        img.src = book["img"]
        slide.appendChild(img)

        const title = document.createElement("h1")
        title.textContent = book["title"]
        slide.appendChild(title)

        const author = document.createElement("h2")
        author.textContent = book["author"]
        slide.appendChild(author)

        carousel.appendChild(slide)
    });
}

const currentSelect = document.getElementById("currentList")
currentSelect.addEventListener("change", () => {
    fillCurrentReading(currentSelect.value)
})

// Do it on load for the default shelf
fillCurrentReading("Reading")