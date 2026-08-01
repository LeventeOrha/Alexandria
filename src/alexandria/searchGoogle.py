"""
Do a Google Books search
"""

import requests
import alexandria.categories as transl
from alexandria.data import Book, Database
from alexandria.img import getColor

class Google:
    def __init__(self, API_key: str, db: Database):
        self.API_key = API_key
        self.db = db

    def searchByIDOnline(self, ID: str) -> dict:
        """
        Search a book by its unique volume ID on Google Books
        """
        url = f"https://www.googleapis.com/books/v1/volumes/{ID}"

        params = {
            "projection": "full",
            "key": self.API_key
        }

        response = requests.get(url, params=params)
        data = response.json()

        return data

    def sparseResults(self, data: dict) -> list[dict]:
        """
        Sparse the results of a Google Books search (too many info)

        Parameters
        ----------
        data: `dict`
            Response of a Google Books API request (one of "items")
        
        Returns
        -------
        book: `dict`
            Dictionary of the book, keys are the titles, with the following
            data: title, author, publish date, image link, Google Books ID, abstract, categories
        """

        book = {}

        book["ID"] = data["id"]

        full_data = self.searchByIDOnline(book["ID"])["volumeInfo"]

        book["title"] = full_data["title"]

        book["author"] = full_data["authors"][0]

        book["date"] = full_data["publishedDate"]

        # As the image sizes are, if alphabetically ordered, are decreasing with each key
        # I rather keep the first one, theoretically the biggest
        image_links = full_data.get("imageLinks", None) # Preparation IF the book doesn't have a cover for some reason
        if image_links is not None:
            book["img"] = image_links[sorted(image_links.keys())[0]].replace("http:", "https:")
        else:
            book["img"] = ""

        categories = full_data.get("categories", None) # There might not be categories
        if categories is not None:
            cats = []
            for cat in categories:
                cat = cat.split("/")
                cat = [c.strip() for c in cat]
                cats += cat

            book["category"] = transl.translateCategories(cats, "en")
        else:
            book["category"] = []

        book["abs"] = full_data.get("description", "")

        return book
    
    def searchBook(self, title: str = "", author: str = "", lang: str = "en") -> list[dict]:
        """
        Search a book on Google Books

        Parameters
        ----------
        title: `str`
            Title of the book
        author: `str`
            Author of the book
        
        Returns
        -------
        response: `list[dict]`
            Response of the request, sparsed
            Each element is a book
        """
        if title == '':
            query = f"inauthor:{author}"
        elif author == "":
            query = f"intitle:{title}"
        else:
            query = f'intitle:{title}+inauthor:{author}'
        url = "https://www.googleapis.com/books/v1/volumes"
        params = {
            "q": query,
            "langRestrict": lang,
            "maxResults": 5,
            "key": self.API_key
        }

        resp = requests.get(url, params=params).json()

        if "items" in resp:
            results = []
            for book in resp["items"]:
                results.append(self.sparseResults(book))
            return results
        else:
            return None

    def searchByID(self, ID: str) -> dict:
        """
        Given an ID, merge the online info (with abstract) with the local info (shelves, ...)
        """
        book_online = self.sparseResults({"id": ID})
        if self.db.bookExists(ID):
            book_stored = self.db.searchBy("ID", ID)[0] # One element list
            book_online["shelf"] = book_stored.shelf
            book_online["start"] = book_stored.start
            book_online["end"] = book_stored.end
            book_online["img"] = book_stored.img # If the SearchByIDOnline returns the wrong image
            book_online["category"] = book_stored.category # To have the in-saved categories show here
        return book_online
    
    def createBook(self, ID: str, shelf: str, start: str = "---", end: str = "---") -> Book:
        """
        Create a new Book instance from an ID and put on a shelf
        """
        b = self.searchByID(ID)

        book = {
            "title": b["title"],
            "author": b["author"],
            "date": b["date"],
            "img": b["img"],
            "ID": ID,
            "category": b["category"],
            "color": getColor(b["img"]),
            "shelf": [shelf],
            "start": start,
            "end": end
        }

        book = Book(**book)

        return book
    
if __name__ == "__main__":
    import alexandria.utils as u
    params = u.readSettings()
    google = Google(u.readSettings(params["API_file"])["GB_API"])

    resp = google.searchBook("The hidden oracle", "Rick Riordan")
    for i in range(len(resp)):
        b = resp[i]
        print(f"{i+1}) {b["title"]} - {b["author"]} ({b["date"]}) - {b["img"]}")

    pick = input("Which book is it actually? (c to cancel, or unique ID if another) ")  
    shelf = input("Which shelf? ")
    start = input("Starting date: ")

    pick = int(pick) -1
    book = google.createBook(resp[pick]["ID"], shelf, start)

    print(book.__repr__())