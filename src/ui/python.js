class Python {
    constructor(){
        // Create the database, moly, google and ai here

        // Dummy result (to not type it down again and again)
        var result = {}
        result["title"] = "Fortuna"
        result["author"] = "Kristyn Merbeth"
        result["date"] = "2019-11-05"
        result["img"] = "http://books.google.com/books/publisher/content?id=aKOHDwAAQBAJ&printsec=frontcover&img=1&zoom=6&edge=curl&imgtk=AFLRE71oTIgVVVf_BIhLPX7Eb8GSL6WCaWQCgjAYcAWfg6RLTPYIHsSlKTvM_uCReMe4WR22dNnxAK542z1F3_PtyGv23Ly3hJ6noUbMLnysdfFlwF3l1p9ge_i_dyt_PA6B1pYcjvNB&source=gbs_api"
        result["ID"] = "aKOHDwAAQBAJ"
        result["shelf"] = ["Reading", "Owned"]
        result["category"] = ["sci-fi"]
        result["start"] = "2026-06-25"
        result["end"] = "---"

        this.book = result
    }

    // Search inside the database, based on any key and value pair
    // (str, str) -> list[dict[str]]
    searchIn(key, value){
        return [this.book, this.book]
    }

    // Search a new book online
    // (str, str, str) -> list[dict[str]]
    searchOut(title, author, lang) {
        return [this.book, this.book]
    }

    // Get details of a book by ID (in database)
    // (str) -> dict[str]
    searchByID(ID) {
        var result = this.book
        results["abstract"] = "This would be the abstract here"

        return result
    }

    // Get all categories
    // () -> list[str]
    getCategories() {
        return ["Fiction", "Science", "History", "Bibliography"]
    }

    // Get all shelves
    // () -> list[str]
    getShelves() {
        return ["Reading", "Read", "To read", "Stopped"]
    }

    // Add a new book to the database
    // (list[dict[str]]) -> None
    addBooks(books) {
        const len = books.length
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
}