class Python {
    constructor(){
        // Create the database, moly, google and ai here

        // Dummy result (to not type it down again and again)
        var fortuna = {}
        fortuna["title"] = "Fortuna"
        fortuna["author"] = "Kristyn Merbeth"
        fortuna["date"] = "2019-11-05"
        fortuna["img"] = "https://books.google.com/books/publisher/content?id=aKOHDwAAQBAJ&printsec=frontcover&img=1&zoom=6&edge=curl&imgtk=AFLRE71oTIgVVVf_BIhLPX7Eb8GSL6WCaWQCgjAYcAWfg6RLTPYIHsSlKTvM_uCReMe4WR22dNnxAK542z1F3_PtyGv23Ly3hJ6noUbMLnysdfFlwF3l1p9ge_i_dyt_PA6B1pYcjvNB&source=gbs_api"
        fortuna["ID"] = "aKOHDwAAQBAJ"
        fortuna["shelf"] = ["Reading", "Owned"]
        fortuna["category"] = ["sci-fi"]
        fortuna["start"] = "2026-06-25"
        fortuna["end"] = "---"

        this.fortuna = fortuna

        var martian = {}
        martian["title"] = "A marsi"
        martian["author"] = "Andy Weir"
        martian["date"] = "2024-06-13"
        martian["img"] = "https://moly.hu/system/covers/big/covers_314900.jpg?1408012841"
        martian["ID"] = "https://moly.hu/konyvek/andy-weir-a-marsi"
        martian["shelf"] = ["Read"]
        martian["category"] = ["novel", "sci-fi", "adventure"]
        martian["start"] = "2026-06-21"
        martian["end"] = "2026-06-28"

        this.martian = martian
    }

    // Search inside the database, based on any key and value pair
    // (str, str) -> list[dict[str]]
    searchIn(key, value){
        return [{ ...this.fortuna }, { ...this.martian }]
    }

    // Search a new book online
    // (str, str, str) -> list[dict[str]]
    searchOut(title, author, lang) {
        return [{ ...this.fortuna }, { ...this.martian }]
    }

    // Get details of a book by ID (in database)
    // (str) -> dict[str]
    searchByID(ID) {
        var result

        if (ID == this.fortuna["ID"]){
            result = { ...this.fortuna }
        } else {
            result = { ...this.martian }
        }

        result["abstract"] = "This would be the abstract here"

        return result
    }

    // Get all categories
    // () -> dict[str] - code name : name in selected language
    getCategories() {
        let categories = {
            "fiction": "Fiction",
            "science": "Science",
            "histroy": "History",
            "bibliography": "Bibliography"
        }
        return categories
    }

    // Get all shelves
    // () -> list[str]
    getShelves() {
        return ["Reading", "Read", "To read", "Stopped"]
    }

    // Add a new books to the database
    // (ids of all books to be added, shelf to place on)
    // (list[str], str) -> None
    addBooks(ids, shelf) {
        const len = ids.length
    }

    // Update a book's data
    // (dict[str]) -> None
    saveBook(book) {
        const keys = Object.keys(book)
    }

    // Delete a book
    // (dict[str]) -> None
    deleteBook(book) {
        const keys = Object.keys(book)
    }

    // Send and recieve a message to the AI assistant
    // (str) -> str
    getAIMessage(user_message){
        return user_message + "\nHello there!"
    }

    // Get the current settings of the system
    // () -> dict[str, str], dict[str, dict[str, str]]
    getSettings() {
        const params = {
            "lang": "en",
            "gemini-model": "gemini-3.5-flash",
            "aiColor": "#008000",
            "userColor": "#00ffff",
            "GUI": true
        }
        const keys = {
            "lang": {
                "en": "English",
                "hu": "Hungarian"
            },
            "gemini-model": {
                "gemini-3.5-flash": "3.5 Flash"
            }
        }
        return [params, keys]
    }


    // Save the new settings
    // (dict[str, str]) -> None
    saveSettings(params) {
        console.log(params)
    }

    // Ask user for a file to SAVE the library into and save it
    // () -> None
    exportLibrary() {
        console.log("Export successful!")
    }

    // Ask user for input file and read in library
    // () -> None
    importLibrary() {
        console.log("Import successful!")
    }
}