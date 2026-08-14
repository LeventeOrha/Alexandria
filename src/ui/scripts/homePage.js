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

function addOneDay(dateString) {
    const d = new Date(dateString);
    d.setDate(d.getDate() + 1);
    return d.toISOString().split("T")[0];
}

async function createCalender() {
    const books = await window.python.getHistory()
    console.log(books)

    const events = await Promise.all(
        books.map(async item => {

            return {
                title: item.title,
                start: item.start,
                end: addOneDay(item.end),
                allDay: true,
                backgroundColor: item.color,
                borderColor: item.color,
                textColor: getTextColor(item.color)
            };
        })
    );

    const calendar = new FullCalendar.Calendar(
        document.getElementById("calendar"),
        {
            initialView: "dayGridMonth",
            height: "auto",
            locale: window.app.settings["Language"],
            fixedWeekCount: false,
            firstDay: 1,
            dayHeaders: true,
            dayHeaderFormat: {
                weekday: "short"   // Mon, Tue, Wed...
            },
            events
        }
    )
    calendar.render()
}
createCalender()

// Fill out a shelf (that given div (ID))
async function fillShelf(divID) {
    // Get the element itself
    const div = document.getElementById(divID)

    // Get the body
    const body = div.querySelector(".shelfBody")

    // Empty it out
    body.replaceChildren()

    // Get the needed shelf
    const shelf = div.querySelector("select").value
    console.log(shelf)

    // Update the database first
    await window.python.updateShelf(shelf)

    // Get the books
    const books = await window.python.listShelf(shelf)
    console.log(JSON.stringify(books, null, 2))

    const MAX_HEIGHT = 250

    // Place them in
    books.forEach(b => {
        if (b["direction"] == 0) { // Spine shown
            const book = document.createElement("div")
            book.id = b["ID"]
            book.textContent = b["title"]
            book.className = "spine"
            book.style.backgroundColor = b["color"]
            book.style.color = getTextColor(b["color"])

            // Add it so the dimensions can be measured
            body.appendChild(book)

            // Measure the minimum height needed
            const minHeight = 2 * book.scrollHeight

            // Pick a random height
            const height = minHeight + Math.random() * (MAX_HEIGHT - minHeight)

            // Set it
            book.style.height = `${height}px`
        }
        else { // Cover image shown
            const book = document.createElement("img")
            book.id = b["ID"]
            book.src = b["img"]
            book.className = "cover"
            body.appendChild(book)
        }
    })
}

document.getElementById("refreshToRead").addEventListener("click", () => {
    fillShelf("toReadShelf")
})
fillShelf("toReadShelf")