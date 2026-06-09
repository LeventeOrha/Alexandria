"""
Search a book on the Moly.hu website (Hungarian books)
"""

import requests
import html
import re
import json
from datetime import datetime
from bs4 import BeautifulSoup
import alexandria.data as d

moly = "https://moly.hu"

hungarian_months = {
    "január": 1,
    "február": 2,
    "március": 3,
    "április": 4,
    "május": 5,
    "június": 6,
    "július": 7,
    "augusztus": 8,
    "szeptember": 9,
    "október": 10,
    "november": 11,
    "december": 12,
}

def parse_hungarian_date(date_str):
    """
    From <év (4)>. <hónap> <nap>. format to actual datetime object
    """
    parts = date_str.strip().split()
    
    year = int(parts[0].rstrip('.'))
    month = hungarian_months[parts[1]]
    day = int(parts[2].rstrip('.'))
    
    return datetime(year, month, day)

def cleanText(text):
    """
    Clear invisible unicode characters from any text
    """
    text = re.sub(r'[\u200b\u200c\u200d\ufeff]', '', text)
    text = ' '.join(text.split())
    return text

def sparseResults(response: str):
    """
    Get the data of one book based on its RELATIVE link to moly.hu

    Returns:
    book: `dict`
        Dictionary containing all important info, with keys: author, title, year, ISBN, all categories, abstract, several image links
    """
    url = moly + response[0]
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)

    # Escaping specific HTML characters, codes and invisible unicode characters
    response = cleanText(html.unescape(response.text))

    soup = BeautifulSoup(response, "html.parser")

    book = {}

    # Get the author
    book["author"] = soup.find(class_ = "authors").contents[0].text

    # Get the title
    book["title"] = soup.find(class_ = "head_title").contents[1].contents[0].text.strip()

    # Get publish dates and ISBN
    editions = soup.find_all(class_ = "edition")
    dates = []
    ISBNS = []
    for edit in editions:
        # Get the date
        date = edit.find("abbr", class_="tooltip")
        if date is None:
            continue
        date = date.get("title").split(": ")[1]
        dates.append(date)

        # Get the ISBN
        divs = edit.find_all("div")
        for div in divs:
            if "ISBN: " in div.text:
                ISBNS.append(f"ISBN{div.text.split("ISBN: ")[1].split(" · ")[0]}")
    
    # Find the newest date
    for i in range(len(dates)):
        dates[i] = parse_hungarian_date(dates[i])
    newest = max(dates)
    book["date"] = newest.strftime("%Y-%m-%d")

    # Get the corresponding ISBN
    book["ID"] = ISBNS[dates.index(newest)]

    # Get ALL categories (sparse later I guess)
    book["category"] = []

    as_ = soup.find(id="book_tags").find("p").contents

    for a in as_:
        txt = a.text
        if txt in ["", " "]:
            continue
        book["category"].append(a.text)

    # Get all image links
    book["imgs"] = []

    imgs = soup.find(id="buyable").find_all(class_ = "zoom")
    for img in imgs:
        lnk = moly + img["href"]
        if lnk not in book["imgs"]:
            book["imgs"].append(lnk)

    # Get abstract
    book["abs"] = ""
    abst = soup.find(class_ = "text shrinkable")
    for p in abst.contents:
        if len(p.text) > 1: # Ignoring empty paragraphs
            book["abs"] += f"{p.text}\n"
    book["abs"] = book["abs"].strip()

    return book

def searchBook(title: str = "", author: str = "", lang: str = "hu"):
    """
    Search query a title and author on Moly (for Hungarian books - language ignored)

    Returns
    -------
    links: `list[str]`
        Each element is a relative link to the actual book's page
    """
    url = moly + "/kereses?utf8=✓&query=" + title.replace(" ", "+").lower() + "+" + author.replace(" ", "+").lower()

    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)

    response = cleanText(html.unescape(response.text))

    soup = BeautifulSoup(response, "html.parser")

    as_ = soup.find_all(class_ = "book_selector")

    links = []

    for a in as_:
        links.append(a.get("href"))

    books = []
    for link in links:
        books.append(sparseResults(link))

    return books

def searchById(ID: str):
    """
    Given one ID, get every data of that book
    """

def createBook(ID: str, shelf: str, start: str = "---", end: str = "---"):
    """
    Create a new book instance that can be straight saved in the database
    """

if __name__ == "__main__":
    books = searchBook("Vörös, fehér és királykék", "Casey McQuiston")