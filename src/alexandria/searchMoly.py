"""
Search a book on the Moly.hu website (Hungarian books)
"""

import requests
import alexandria.data as d

moly = "https://moly.hu"

def searchBook(title: str, author: str):
    """
    Search query a title and author on Moly

    Returns
    -------
    links: `list[str]`
        Each element is a link to the actual book's page
    """
    url = moly + "/kereses?utf8=✓&query=" + title.replace(" ", "+").lower() + "+" + author.replace(" ", "+").lower()

    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)

    response = response.text.split("<table>")[1]
    response = response.split("</table>")[0]
    response = response.split('</div>')[2]
    response = response.split('</td>')[0]

    response = response.replace("<p>", "")

    response = response.split("</p>")

    links = []
    
    for a in response:
        if "href" in a:
            links.append(a.split('href="')[1].split('"')[0])

    return links

    with open("moly.dat", "wt", encoding='utf-8') as out:
        out.write(str(links))

def getBookMoly(link: str):
    """
    Get the data based on its RELATIVE link to moly.hu

    Returns:
    book: `dict`
        Dictionary containing all important info, with keys same as alexandria.data.Book class
    """
    url = moly + link
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)

    with open("moly.dat", "wt", encoding='utf-8') as out:
        out.write(response.text)

if __name__ == "__main__":
    links = searchBook("Vörös, fehér és királykék", "Casey McQuiston")
    getBookMoly(links[0])