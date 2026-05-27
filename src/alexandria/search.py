"""
File to do a Google Books search
"""

import requests
import json
from alexandria.utils import *

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
    books = {}

    for data in response["items"]:
        book = {}
        book["title"] = data["volumeInfo"]["title"]
        book["author"] = data["volumeInfo"]["authors"]
        book["date"] = data["volumeInfo"]["publishedDate"]
        if "imageLinks" in data["volumeInfo"]:
            book["img"] = data["volumeInfo"]["imageLinks"].get("thumbnail", None)
        else:
            book["img"] = None
        book["ID"] = data["id"]

        books[book["title"]] = book

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

if __name__ == "__main__":

    title = "A harmadik lány"
    author = "Agatha Christie"

    resp = searchBookOnGoogle(title, author)

    with open('data.json', "wt", encoding="utf-8") as out:
        json.dump(resp, out, indent=4, sort_keys=True, ensure_ascii=False)