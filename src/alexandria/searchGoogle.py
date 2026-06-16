"""
Do a Google Books search
"""

import requests
import alexandria.categories as transl
from alexandria.data import Book

class Google:
    def __init__(self, API_key: str):
        self.API_key = API_key

    def sparseResults(self, response: dict) -> list[dict]:
        """
        Sparse the results of a Google Books search (too many info)

        Parameters
        ----------
        response: `dict`
            Response of a Google Books API request
        
        Returns
        -------
        books: `list`
            Dictionary of each book, keys are the titles, with the following
            data: title, author, publish date, image link, Google Books ID
        """

        books = []

        for data in response["items"]:
            book = {}
            book["title"] = data["volumeInfo"].get("title")
            book["author"] = data["volumeInfo"].get("authors")
            book["date"] = data["volumeInfo"].get("publishedDate")
            if "imageLinks" in data["volumeInfo"]:
                book["img"] = data["volumeInfo"]["imageLinks"].get("thumbnail", None)
            else:
                book["img"] = None
            book["ID"] = data["id"]
            book["lang"] = data["volumeInfo"]["language"]

            books.append(book)

        return books
    
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
            return self.sparseResults(resp)
        else:
            return None
        
    def searchByID(self, ID: str) -> dict:
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
    
    def createBook(self, ID: str, shelf: str, start: str = "---", end: str = "---") -> Book:
        """
        Create a new Book instance from an ID and put on a shelf
        """
        info = self.searchByID(ID)

        book = {}
        book["title"] = info["volumeInfo"]["title"]
        book["author"] = info["volumeInfo"]["authors"][0]
        book["date"] = info["volumeInfo"]["publishedDate"]

        # As the image sizes are, if alphabetically ordered, are decreasing with each key
        # I rather keep the first one, theoretically the biggest
        book["img"] = info["volumeInfo"]["imageLinks"][sorted(info["volumeInfo"]["imageLinks"].keys())[0]]

        book["ID"] = ID
        book["category"] = []
        book["shelf"] = [shelf]

        categories = []
        for category in info["volumeInfo"]["categories"]:
            cat = category.split(" / ")
            for c in cat:
                categories.append(c.strip())
        book["category"] = transl.translateCategories(categories, "en")

        book["start"] = start
        book["end"] = end

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