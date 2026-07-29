"""
Search a book on OpenLibrary
"""

import json
import requests
from alexandria.data import Book, Database
import alexandria.categories as transl

class OpenLibrary:
    def __init__(self, db: Database):
        self.db = db
        self.url = "https://openlibrary.org"
        self.covers_olid = "https://covers.openlibrary.org/b/olid/"
        self.covers_id = "https://covers.openlibrary.org/b/id/"
        self.timeout = 500

    def sparseResults(self, resp: dict) -> dict[str]:
        """
        Sparse a book object from a response - and get each edition as a different book
        """
        url = f"{self.url}/{resp["key"]}/editions.json"
        editions = json.loads(requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=self.timeout).text)

        url = f"{self.url}{resp["key"]}.json"
        categories = json.loads(requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=self.timeout).text).get("subjects", [])
        categories = transl.translateCategories(categories, "en")

        needed_keys = ["covers", "key", "publish_date", "title", "authors"]

        books = []
        for edition in editions["entries"]:
            if edition.get("physical_format", "").lower() == "audiobook":
                continue
            if all(key in edition for key in needed_keys):
                book = {}
                book["img"] = f"{self.covers_id}{edition["covers"][0]}-L.jpg"
                book["ID"] = edition["key"]
                book["abs"] = edition.get("description", "No abstract found.")
                book["date"] = edition["publish_date"]
                book["title"] = edition["title"]

                url = f"{self.url}{edition["authors"][0]["key"]}.json"
                authorData = json.loads(requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=self.timeout).text)
                book["author"] = authorData.get("personal_name", authorData.get("name", ""))

                books.append(book)
        
        return books

    def searchBook(self, title: str, author: str, lang: str) -> list[dict[str]]:
        """
        Search query anything on OpenLibrary

        Returns
        -------
        links: `list[Book]`
            Each element is complete Book object
        """
        url = self.url + f"/search.json?title={title.replace(" ", "+").lower()}&author={author.replace(" ", "+").lower()}&lang={lang}"

        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=self.timeout)

        response = json.loads(response.text)

        if response["numFound"] < 1:
            return None
        else:
            books = []
            for book in response["docs"]:
                books += self.sparseResults(book)
            return books

    def searchByID(self, ID: str) -> dict[str]:
        """
        Get all data of a book based on an ID
        """
        url = self.url + ID + ".json"
        resp = json.loads(requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=self.timeout).text)

        book = {}

        book["title"] = resp["title"]

        authorData = self.url + resp["authors"][0]["key"] + ".json"
        authorData = json.loads(requests.get(authorData, headers={"User-Agent": "Mozilla/5.0"}, timeout=self.timeout).text)
        book["author"] = authorData.get("personal_name", authorData.get("name", ""))

        book["date"] = resp["publish_date"]

        book["img"] = f"{self.covers_id}{resp["covers"][0]}-L.jpg"

        book["ID"] = ID

        workID = resp["works"][0]["key"]
        workData = self.url + workID + ".json"
        workData = json.loads(requests.get(workData, headers={"User-Agent": "Mozilla/5.0"}, timeout=self.timeout).text)

        book["category"] = transl.translateCategories(workData.get("subjects", []), "en") # Safeguarding if there is no "subjects"

        book["shelf"] = []
        book["start"] = "---"
        book["end"] = "---"

        if self.db.bookExists(ID):
            book_stored = self.db.searchBy("ID", ID)[0]
            book["shelf"] = book_stored.shelf
            book["start"] = book_stored.start
            book["end"] = book_stored.end
            book["category"] = book_stored.category

        return book

    def createBook(self, ID: str, shelf: str, start: str = "---", end: str = "---") -> Book:
        b = self.searchByID(ID)
        b["shelf"] = [shelf]
        b["start"] = start
        b["end"] = end

        return Book(**b)


if __name__ == "__main__":
    db = Database("../../datafiles/books.db")
    ol = OpenLibrary(db)
    print(ol.searchBook("Floating hotel", "Grace Curtis", "en"))