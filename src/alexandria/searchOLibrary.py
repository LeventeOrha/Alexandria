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
        Sparse a book object from a response
        """
        book = {}

        book["title"] = resp["title"]
        book["author"] = resp["author_name"][0] if type(resp["author_name"]) is list else resp["author_name"]

        book["date"] = resp["first_publish_year"]

        book["img"] = self.covers_olid + resp["cover_edition_key"] + "-L.jpg"

        book["ID"] = "/books/" + resp["cover_edition_key"]

        url = self.url + book["ID"] + ".json"
        resp = json.loads(requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=self.timeout).text)
        categories = resp["subjects"]
        book["category"] = transl.translateCategories(categories)

        return book

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
                books.append(self.sparseResults(book))
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
        book["author"] = authorData["name"]

        book["date"] = resp["publish_date"]

        book["img"] = f"{self.covers_id}{resp["covers"][0]}-L.jpg"

        book["ID"] = ID

        book["category"] = transl.translateCategories(resp["subjects"], "en")

        return book

    def createBook(self, ID: str, shelf: str, start: str = "---", end: str = "---") -> Book:
        b = self.searchByID(ID)
        b["shelf"] = shelf
        b["start"] = start
        b["end"] = end

        return Book(**b)


if __name__ == "__main__":
    db = Database("../../datafiles/books.db")
    ol = OpenLibrary(db)
    print(ol.searchBook("Floating hotel", "Grace Curtis", "en"))