"""
File to do a Google Books search
"""

import requests
import sys
from alexandria.utils import *
from alexandria.data import *

def sparseResultsOfGoogle(response: dict):
    """
    Sparse the results of a Google Books search (too many info)

    Parameters
    ----------
    response: `dict`
        Response of a Google Books API request
    
    Returns
    -------
    books: `dict`
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

        books.append(book)

    return books

def searchBookOnGoogle(title: str = "", author: str = ""):
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
    response: `dict`
        Response of the request, sparsed
        Each key is a title
    """
    params = readSettings()
    if title == '':
        query = f"inauthor:{author}"
    elif author == "":
        query = f"intitle:{title}"
    else:
        query = f'intitle:{title}+inauthor:{author}'
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {"q": query, "maxResults": 5, "key": params["GB_API"]}

    resp = requests.get(url, params=params).json()

    if "items" in resp:
        return sparseResultsOfGoogle(resp)
    else:
        return None
    
def searchByID(ID: str):
    """
    Search a book by its unique volume ID on Google Books
    """
    params = readSettings()
    url = f"https://www.googleapis.com/books/v1/volumes/{ID}"

    params = {
        "projection": "full",
        "key": params["GB_API"]
    }

    response = requests.get(url, params=params)
    data = response.json()

    return data

def createBook(ID: str, category: str, start: str = "---", end: str = "---"):
    info = searchByID(ID)

    book = {}
    book["title"] = info["volumeInfo"]["title"]
    book["author"] = info["volumeInfo"]["authors"][0]
    book["date"] = info["volumeInfo"]["publishedDate"]

    # As the image sizes are, if alphabetically ordered, are decreasing with each key
    # I rather keep the first one, theoretically the biggest
    book["img"] = sorted(info["volumeInfo"]["imageLinks"].keys())[0]

    book["ID"] = ID
    book["category"] = []
    book["genre"] = []

    for category in info["volumeInfo"]["categories"]:
        cat = category.split(" / ")[1]
        if cat not in book["genre"]:
            book["genre"].append(cat)

    book["start"] = start
    book["end"] = end

    book = Book(**book)

    return book

if __name__ == "__main__":

    if ("-t" not in sys.argv) or ("-a" not in sys.argv):
        print(f"Useage: {sys.argv[0]} -t <title> -a <author> -l <language>")
        exit()
    
    title = " ".join(sys.argv).split("-t")[1].split("-a")[0].strip()
    author = " ".join(sys.argv).split("-t")[1].split("-a")[1].strip()

    resp = searchBookOnGoogle(title, author)

    for i in range(len(resp)):
        b = resp[i]
        print(f"{i+1}) {b["title"]} - {b["author"]} ({b["date"]}) - {b["img"]}")

    pick = input("Which book is it actually? (c to cancel) ")  
    if pick.lower() == "c":
        exit()  

    pick = int(pick) - 1
    cat = input("Which category? ")
    start = input("Starting date: ")

    book = createBook(resp[i]["ID"], cat, start)

    if bookExists(book.ID):
        a = input(f"This book is already saved. Do you want to update the category and starting date? (y/n)")
        if a == "y":
            updateBook(book)
    else:
        addBooks([book])
