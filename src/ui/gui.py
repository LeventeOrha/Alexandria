import webview
import tkinter as tk
from tkinter import filedialog
import os
from dataclasses import asdict
import yaml
import json

from alexandria.data import Book, Database
import alexandria.utils as au
from alexandria.searchGoogle import Google
from alexandria.searchMoly import Moly
from alexandria.searchOLibrary import OpenLibrary
from alexandria.ai import AI
import alexandria.categories as acats

class API:
    def __init__(self, params: dict):
        """
        Create a new Graphical User Interface using libary
        Also setting up things if newly installed
        """
        # Get screen width and height (for placing and sizing later)
        root = tk.Tk()
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        root.destroy()

        # Read in parameter files
        self.params = params
        self.ai_settings = au.readSettings(params["AI_settings"])

        # Read in text file
        text = self.readYML(params["GUI_text_file"])
        self.text = text[params["Language"]]
        self.settings_options = text["Options"]

        # Creating sub-classes (database, searches)
        self.db = Database(params["datafile"])
        self.moly = Moly(self.db)
        self.ol = OpenLibrary(self.db)

        # Check out if the API key file is found
        if os.path.exists(params["API_file"]):
           # Then create Google Books and Gemini
           self.setUpWithKeys() 

    def readYML(self, file: str) -> dict[str]:
        """
        Reading a .yml/.yaml file
        """
        with open(file, 'rt', encoding="utf-8") as inp:
            text = yaml.safe_load(inp)
        return text

    def setUpWithKeys(self):
        """
        Set up Google Books API and AI agent when there are actual keys
        """
        # Read in keys
        self.api_keys = au.readSettings(self.params["API_file"])

        # Create Google Books API
        self.gb = Google(self.api_keys["GB_API"], self.db)

        # Create AI agent (Gemini throws error if there is no key)
        self.ai = AI(self.api_keys, self.params["Gemini_model"], self.ai_settings, self.db)

    def isNewUser(self) -> bool:
        """
        Check out if this is a new user or not
        """
        return self.db.is_new

    def searchIn(self, key: str, value: str) -> list[dict[str, str]]:
        """
        Search inside the database, based on any key and value pair
        """
        books = self.db.searchBy(key, value)
        for i in range(len(books)):
            books[i] = asdict(books[i])
        return books

    def searchOut(self, title: str, author: str, lang: str) -> list[dict[str, str]]:
        """
        Search a new book online
        """
        if lang == "hu":
            books = self.moly.searchBook(title, author)
        else:
            books = self.gb.searchBook(title, author, lang)

            if books is None:
                books = self.ol.searchBook(title, author, lang)
            if books is None:
                return None
        return books

    def searchByID(self, ID: str) -> dict[str]:
        """
        Get details of a single book already in the database
        """
        if "moly" in ID:
            book = self.moly.searchByID(ID)
        elif "OL" in ID:
            book = self.ol.searchByID(ID)
        else:
            book = self.gb.searchByID(ID)
        return book

    def getCategories(self) -> dict[str]:
        """
        Get all categories in (code name) : (name in selected language) format
        """
        categories = acats.readCategories()["categories"]
        cats = {}

        lang = self.params["Language"]

        for key in categories:
            cats[key] = categories[key][lang]

        return cats

    def getShelves(self) -> list[str]:
        """
        Get all shelves
        """
        return self.db.getShelves()

    def addBooks(self, ids: list[str], shelf: str) -> None:
        """
        Add new books to the database

        Parameters
        ----------
        ids: `list[str]`
            IDs of the books to be added
        shelf: `str`
            Shelf to place these books on
        """
        books = []
        for ID in ids:
            if "moly" in ID:
                book = self.moly.createBook(ID, shelf, 0)
            elif "OL" in ID:
                book = self.ol.createBook(ID, shelf)
            else:
                book = self.gb.createBook(ID, shelf)
            books.append(book)
        self.db.addBooks(books)
        return
    
    def saveBook(self, b: dict[str]) -> None:
        """
        Update a book's data
        """

        book = {
            "title": b["title"],
            "author": b["author"],
            "date": b["date"],
            "img": b["img"],
            "ID": b["ID"],
            "category": b["category"],
            "shelf": b["shelf"],
            "start": b["start"],
            "end": b["end"]
        }

        book = Book(**book)

        self.db.updateBook(book)
        return

    def deleteBook(self, book: dict[str]) -> None:
        """
        Delete a book
        """
        self.db.removeBook(book["ID"])
        return

    def getAIMessage(self, user_message: str) -> str:
        """
        Send and recieve a message to the AI assistant
        """
        if hasattr(self, "ai") is False:
            return self.text["AiMessages"]["NoAIConnection"]
        try:
            response = self.ai.generateResponse(user_message)
            return response
        except:
            return self.text["AiMessages"]["FailedAIMessage"]

    def getSettings(self) -> tuple[dict[str], dict[str]]:
        """
        Get the current settings of the system

        Returns
        -------
        params: `dict[str]`
            Current, overall settings of the system
        keys: `dict[str]`
            Options for the different settings
        """
        params = self.params.copy()
        params["GBooksAPIkey"] = self.api_keys["GB_API"]
        params["GeminiAPI"] = self.api_keys["Gemini_API"]

        return params, self.settings_options

    def getText(self, lang: str) -> dict[str]:
        """
        Read in the given language text
        """
        return self.text

    def saveSettings(self, params: dict) -> None:
        """
        Save the new settings
        """
        # Merge the two params dict, fusing the new info into the old - discarding new keys
        for key in self.params.keys() & params.keys():
            self.params[key] = params[key]

        # Save API keys
        self.api_keys["GB_API"] = params["GBooksAPIkey"]
        self.api_keys["Gemini_API"] = params["GeminiAPI"]

        # Write them out into the file
        with open(self.params["API_file"], "wt", encoding="utf-8") as out:
            json.dump(self.api_keys, out, ensure_ascii=False, indent=4)

        # Save the parameters
        au.writeSettings(self.params)
        return

    def exportLibrary(self) -> str:
        """
        Ask user for a file to SAVE the library into and save it
        """
        root = tk.Tk()
        root.withdraw() # Hide the main window

        filePath = filedialog.asksaveasfilename(
            title = self.text["exportLibraryTo"],
            defaultextension = ".csv",
            filetypes = [
                ("CSV files", "*.csv"),
                ("YAML files", "*.yaml")
            ]
        )
        root.destroy() # close tkinter

        # File extension given by user
        ext = filePath.rsplit(".", 1)[1]

        if ext == "csv":
            self.db.exportCSV(filePath)
        elif ext == "yaml":
            self.db.exportYML(filePath)
        else:
            return self.text["failedExport"]
        return self.text["successfulExport"]

    def importLibrary(self) -> str:
        """
        Ask user for input file and read in library
        """
        root = tk.Tk()
        root.withdraw() # Hide the main window

        filePath = filedialog.askopenfilename(
            title = self.text["importLibraryFrom"],
            filetypes = [
                ("CSV files", "*.csv"),
                ("All files", "*.*")
            ]
        )
        root.destroy() # close tkinter

        # Check file extension
        if filePath.rsplit(".", 1)[1] == "csv":
            self.db.importCSV(filePath)
            return self.text["successfulImport"]
        return self.text["failedImport"]

    def backgroundChange(self) -> str:
        """
        Ask a user for an image file as a background, returning filename
        """
        root = tk.Tk()
        root.withdraw() # Hide the main window

        filePath = filedialog.askopenfilename(
            title = self.text["backgroundImage"],
            filetypes = [
                ("PNG files", "*.png"),
                ("JPG files", "*.jpg"),
                ("JPEG files", "*.jpeg"),
                ("SVG files", "*.svg")
            ]
        )
        root.destroy() # close tkinter
        # Check file extension
        if filePath.rsplit(".", 1)[1] in ["png", "jpg", "jpeg", "svg"]:
            self.params["background"] = filePath
            return filePath

def main(params: dict, debug: bool = False):
    api = API(params)

    window = webview.create_window(
        "Alexandria", "./src/ui/index.html",
        width = api.screen_width * 0.8,
        height = api.screen_height * 0.8,
        x = (api.screen_width - api.screen_width * 0.8) // 2,
        y = (api.screen_height - api.screen_height * 0.8) // 2,
        js_api = api
    )

    webview.start(debug=debug) # For debugging tools