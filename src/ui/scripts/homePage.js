// Fill out the carousel at currentReading
const currentSelect = document.getElementById("currentList")

async function fillCurrentReading(shelf) {
    const books = await window.python.searchIn("shelf", shelf)

    const carousel = document.getElementById("currentBody")
    carousel.replaceChildren() // Empty it out

    // Jump back to the first slide
    carousel.scrollTo({
        left: 0,
        behavior: "auto"
    })

    books.forEach(book => {
        const slide = document.createElement("div")
        slide.className = "slide"

        const img = document.createElement("img")
        img.src = book["img"]
        
        img.addEventListener("click", async (event) => {
            const b = await window.python.searchByID(book["ID"]) // Get the book info

            event.stopPropagation()

            document.querySelector(".searchResults").replaceChildren()

            document.getElementById("searchButton").click() // Switch to search page

            await fillBookData(b)
        })

        slide.appendChild(img)

        const title = document.createElement("h1")
        title.textContent = book["title"]
        slide.appendChild(title)

        const author = document.createElement("h2")
        author.textContent = book["author"]
        slide.appendChild(author)

        carousel.appendChild(slide)
    });
    currentSelect.value = shelf
}

currentSelect.addEventListener("change", () => {
    fillCurrentReading(currentSelect.value)
})

// Do it on load for the default shelf
fillCurrentReading("Reading")

// Attatch scrolling to the carousel
const currentBody = document.getElementById("currentBody")
currentBody.addEventListener("wheel", (e) => {
    e.preventDefault();

    const slides = currentBody.querySelectorAll(".slide");
    const slideWidth = currentBody.clientWidth;

    const current = Math.round(currentBody.scrollLeft / slideWidth);

    let next = current;

    if (e.deltaY > 0) {
        next = Math.min(current + 1, slides.length - 1);
    } else if (e.deltaY < 0) {
        next = Math.max(current - 1, 0);
    }

    currentBody.scrollTo({
        left: next * slideWidth,
        behavior: "smooth"
    });
}, { passive: false });

// Make the current reading div clickable, pointing to the "this shelf search" part
document.getElementById("currentReading").addEventListener("click", (event) => {
    if (event.target.closest("select, button, input, textarea, a, img")) {return}

    const shelf = document.getElementById("currentList").value

    // Set in the values to search for
    document.getElementById("searchKey").value = "shelf"
    document.getElementById("searchValue").value = shelf

    // Transfer to that main and do the search
    document.getElementById("searchButton").click()
    document.getElementById("startSearch").click()
})