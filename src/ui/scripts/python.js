class Python {
    // Class to handle API connection easier
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
    async searchIn(key, value){
        let result

        if (window.pywebview?.api) {
            result = await window.pywebview.api.searchIn(key, value)
        }
        else {
            result = [{ ...this.fortuna }, { ...this.martian }]
        }
        return result
    }

    // Search a new book online
    // (str, str, str) -> list[dict[str]]
    async searchOut(title, author, lang) {
        let result

        if (window.pywebview?.api) {
            result = await window.pywebview.api.searchOut(title, author, lang)
        }
        else {
            result = [{ ...this.fortuna }, { ...this.martian }]
        }
        return result
    }

    // Get details of a book by ID (in database)
    // (str) -> dict[str]
    async searchByID(ID) {
        let result

        if (window.pywebview?.api) {
            result = await window.pywebview.api.searchByID(ID)
        }
        else {
            result = [{ ...this.fortuna }, { ...this.martian }]
        }
        return result
    }

    // Get all categories
    // () -> dict[str] - code name : name in selected language
    async getCategories() {
        let result

        if (window.pywebview?.api) {
            result = await window.pywebview.api.getCategories()
        }
        else {
            result = {
                "fiction": "Fiction",
                "science": "Science",
                "histroy": "History",
                "bibliography": "Bibliography"
            }
        }
        return result
    }

    // Get all shelves
    // () -> list[str]
    async getShelves() {
       let result

        if (window.pywebview?.api) {
            result = await window.pywebview.api.getShelves()
        }
        else {
            result = ["Reading", "Read"]
        }
        return result
    }

    // Get all books on a specific shelf with their display direction
    // (str) -> list[dict[str]]
    async listShelf(shelf) {
        let result

        if (window.pywebview?.api) {
            result = await window.pywebview.api.listShelf(shelf)
        }
        else {
            result = [{ ...this.fortuna }, { ...this.martian }]
        }
        return result
    }

    // Update the shelf database based on the books db
    // (str) -> None
    async updateShelf(shelf) {
       if (window.pywebview?.api) {
            await window.pywebview.api.updateShelf(shelf)
       }
    }

    // Rotate a book (toggle its direction)
    // (str, str) -> None
    async rotateBook(shelf, ID) {
        if (window.pywebview?.api) {
            await window.pywebview.api.rotateBook(shelf, ID)
        }
    }

    // Add a new books to the database
    // (ids of all books to be added, shelf to place on)
    // (list[str], str, list[str]) -> None
    async addBooks(ids, shelf, imgs) {
        await window.pywebview.api.addBooks(ids, shelf, imgs)
    }

    // Update a book's data
    // (dict[str]) -> None
    async saveBook(book) {
        await window.pywebview.api.saveBook(book)
    }

    // Delete a book
    // (dict[str]) -> None
    async deleteBook(book) {
        await window.pywebview.api.deleteBook(book)
    }

    // Send and recieve a message to the AI assistant
    // (str) -> str
    async getAIMessage(user_message){
        let result

        if (window.pywebview?.api) {
            result = await window.pywebview.api.getAIMessage(user_message)
        }
        else {
            result = "Sorry, something went wrong. Try again!"
        }
        return result
    }

    // Get the current settings of the system
    // () -> dict[str, str], dict[str, dict[str, str]]
    async getSettings() {
        let params, keys

        if (window.pywebview?.api) {
            [params, keys] = await window.pywebview.api.getSettings()
        }
        else {
            params = {
                "Language": "hu",
                "Gemini_model": "gemini-3.5-flash",
                "aiColor": "#008000",
                "userColor": "#00ffff",
                "GUI-useage": true,
                "background": "../images/bookshelf_background.jpg",
                "GBooksAPIkey": "AbAc",
                "GeminiAPI": "GeMiNiKeY"
            }
            keys = {
                "Language": {
                    "en": "English",
                    "hu": "Hungarian"
                },
                "Gemini_model": {
                    "gemini-3.5-flash": "3.5 Flash"
                }
            }
        }
        return [params, keys]
    }

    // Read in given language text
    // (str) -> dict[str: str]
    async getText(lang) {
        if (window.pywebview?.api) {
            let result
            result = await window.pywebview.api.getText(lang)
            return result
        }
        else {
            const text = {
                "hu": {
                    "placeholders": {
                        "onlineTitle": "Cím",
                        "onlineAuthor": "Író",
                    },
                    "textContents": {
                        "saveBooksOnShelf": "Mentés",
                        "searchKeyTitle": "Cím",
                        "searchKeyAuthor": "Író",
                        "searchKeyShelf": "Polc",
                        "searchKeyCategory": "Kategória",
                        "languageSetting": "Nyelv:",
                        "aiChatColorSetting": "Könyváros színe:",
                        "userChatColorSetting": "Felhasználó színe:",
                        "backgroundImageSetting": "Háttérkép:",
                        "GUISetting": "Vizuális felület",
                        "saveSettings": "Mentés",
                        "exportLibrary": "Könyvtár exportálása", 
                        "importLibrary": "Könyvtár importálása",
                    },
                    "inCodeOptions": {
                        "bookStart": "Kezdve",
                        "bookEnd": "Befejezve",
                        "edit": "Szerkesztés",
                        "delete": "Törlés",
                        "save": "Mentés",
                        "categories": "Kategóriák",
                        "shelves": "Polcok",
                        "new": "Új"
                    }
                },
                "en": {
                    "placeholders": {
                        "onlineTitle": "Title",
                        "onlineAuthor": "Author",
                    },
                    "textContents": {
                        "saveBooksOnShelf": "Save",
                        "searchKeyTitle": "Title",
                        "searchKeyAuthor": "Author",
                        "searchKeyShelf": "Shelf",
                        "searchKeyCategory": "Category",
                        "languageSetting": "Language:",
                        "aiChatColorSetting": "Librarian chat color:",
                        "userChatColorSetting": "User chat color:",
                        "backgroundImageSetting": "Background image:",
                        "GUISetting": "Graphical interface",
                        "saveSettings": "Save",
                        "exportLibrary": "Export library", 
                        "importLibrary": "Import library",
                    },
                    "inCodeOptions": {
                        "bookStart": "Start",
                        "bookEnd": "End",
                        "edit": "Edit",
                        "delete": "Delete",
                        "save": "Save",
                        "categories": "Categories",
                        "shelves": "Shelves",
                        "new": "New"
                    }
                }
            }
            return text[lang]
        }
    }


    // Save the new settings
    // (dict[str, str]) -> None
    async saveSettings(params) {
        await window.pywebview.api.saveSettings(params)
    }

    // Ask user for a file to SAVE the library into and save it
    // () -> None
    async exportLibrary() {
        await window.pywebview.api.exportLibrary()
    }

    // Ask user for input file and read in library
    // () -> None
    async importLibrary() {
        await window.pywebview.api.importLibrary()
    }

    // Ask user for an image file as a background, returning the filename
    // () -> str
    async backgroundChange() {
       let result

       if (window.pywebview?.api) {
        result = await window.pywebview.api.backgroundChange()
       }
       else {
        result = "./images/bookshelf_background.jpg"
       }
       return result
    }

    // Check if this is a new user (Newly created database)
    // () -> bool
    async isNewUser() {
        let result

        if (window.pywebview?.api) {
            result = await window.pywebview.api.isNewUser()
        }
        else {
            result = false
        }
        return result
    }

    //Get a list of all books that have at least "start"
    // () -> list[dict[str, str]]
    async getHistory() {
        let result

        if (window.pywebview?.api) {
            result = await window.pywebview.api.getHistory()
        }
        else {
            result = [{...this.fortuna}, {...this.martian}]
        }
        return result
    }
}