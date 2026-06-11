"""
File to do a Google Books search
"""

import requests
import sys
from alexandria.utils import *
from alexandria.data import *
import alexandria.categories as transl

def sparseResults(response: dict):
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

def searchBook(title: str = "", author: str = "", lang: str = "en"):
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
    params = readSettings()
    API_KEY = readSettings(params["API_file"])["GB_API"]
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
        "key": API_KEY
    }

    resp = requests.get(url, params=params).json()

    if "items" in resp:
        return sparseResults(resp)
    else:
        return None
    
def searchByID(ID: str):
    """
    Search a book by its unique volume ID on Google Books
    """
    params = readSettings()
    API_KEY = readSettings(params["API_file"])["GB_API"]
    url = f"https://www.googleapis.com/books/v1/volumes/{ID}"

    params = {
        "projection": "full",
        "key": API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    return data

def createBook(ID: str, shelf: str, start: str = "---", end: str = "---"):
    info = searchByID(ID)

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
    print(categories)
    book["category"] = transl.translateCategories(categories, "en")

    book["start"] = start
    book["end"] = end

    book = Book(**book)

    return book

if __name__ == "__main__":

    if len(sys.argv) != 4:
        print(f"Useage: {sys.argv[0]} -t <title> -a <author> -l <language>")
        exit()
    
    title = sys.argv[1]
    author = sys.argv[2]
    lang = sys.argv[3]

    resp = searchBook(title, author, lang)

    for i in range(len(resp)):
        b = resp[i]
        if b["lang"] != lang: # Ignoring books if (for some reason) wrong language results are returned
            continue
        print(f"{i+1}) {b["title"]} - {b["author"]} ({b["date"]}) - {b["img"]}")

    pick = input("Which book is it actually? (c to cancel, or unique ID if another) ")  
    if pick.lower() == "c":
        exit()  
    try:
        pick = int(pick) - 1
    except ValueError:
        pass
    shelf = input("Which shelf? ")
    start = input("Starting date: ")

    try:
        pick = int(pick) -1
        book = createBook(resp[pick]["ID"], shelf, start)
    except ValueError:
        book = createBook(pick, shelf, start)

    if bookExists(book.ID):
        a = input(f"This book is already saved. Do you want to update the shelf and starting date? (y/n)")
        if a == "y":
            updateBook(book)
    else:
        addBooks([book])

    print("Book succesfully added to database!")

    exportCSV("book.csv")