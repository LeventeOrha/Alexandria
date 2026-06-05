from dataclasses import dataclass, asdict
from typing import List
import sqlite3
import json
from alexandria import utils as u

# Default value for the 
DATAFILE = u.readSettings()["datafile"]

@dataclass
class Book:
    title: str
    author: str
    date: str
    img: str
    ID: str
    category: List[str]
    genre: List[str]
    start: str
    end: str

    def __str__(self):
        return f"{self.title} by {self.author}"

    def __repr__(self):
        s = f"Book:\n"
        s += f"\ttitle: {self.title}\n"
        s += f"\tauthor: {self.author}\n"
        s += f"\tdate: {self.date}\n"
        s += f"\timg: {self.img}\n"
        s += f"\tID: {self.ID}\n"
        s += f"\tcategory: {self.category}\n"
        s += f"\tgenre: {self.genre}\n"
        s += f"\tstart: {self.start}\n"
        s += f"\tend: {self.end}\n"
        return s


def get_connection():
    """
    Create SQL connection to datafile (books.db)
    """
    conn = sqlite3.connect(DATAFILE)
    conn.row_factory = sqlite3.Row
    return conn


def createDatabase():
    """
    Create database table
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS books (
        ID TEXT PRIMARY KEY,
        title TEXT,
        author TEXT,
        date TEXT,
        img TEXT,
        category TEXT,
        genre TEXT,
        start TEXT,
        end TEXT
    )
    """)

    conn.commit()
    conn.close()


def row_to_book(row):
    """
    Convert SQLite row to Book object
    """
    data = dict(row)

    data["category"] = json.loads(data["category"])
    data["genre"] = json.loads(data["genre"])

    return Book(**data)


def addBooks(books: list[Book]):
    """
    Add many books to the database
    """
    conn = get_connection()
    cur = conn.cursor()

    data = []

    for book in books:
        data.append((
            book.ID,
            book.title,
            book.author,
            book.date,
            book.img,
            json.dumps(book.category),
            json.dumps(book.genre),
            book.start,
            book.end
        ))

    cur.executemany("""
    INSERT OR IGNORE INTO books
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, data)

    conn.commit()
    conn.close()


def updateBook(book: Book):
    """
    Update the data of one book
    """
    data = asdict(book)

    data["category"] = json.dumps(book.category)
    data["genre"] = json.dumps(book.genre)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    UPDATE books
    SET
        title = :title,
        author = :author,
        date = :date,
        img = :img,
        category = :category,
        genre = :genre,
        start = :start,
        end = :end
    WHERE ID = :ID
    """, data)

    conn.commit()
    conn.close()


def removeBook(book: Book):
    """
    Remove a book from the database
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    DELETE FROM books
    WHERE ID = ?
    """, (book.ID,))

    conn.commit()
    conn.close()


def searchBy(key: str, value: str):
    """
    Search all books by a specific key/value pair

    Parameters
    ----------
    key: str
        Column name
    value: str
        Value to search for

    Returns
    -------
    list[Book]
    """
    conn = get_connection()
    cur = conn.cursor()

    allowed_columns = {
        "ID",
        "title",
        "author",
        "date",
        "img",
        "start",
        "end"
    }

    if key not in allowed_columns:
        raise ValueError("Invalid column name")

    cur.execute(
        f"SELECT * FROM books WHERE {key} = ?",
        (value,)
    )

    rows = cur.fetchall()

    conn.close()

    return [row_to_book(row) for row in rows]


def searchByGenre(genre: str):
    """
    Search books containing a genre
    """
    books = getAllBooks()

    return [
        book for book in books
        if genre in book.genre
    ]


def searchByCategory(category: str):
    """
    Search books containing a category
    """
    books = getAllBooks()

    return [
        book for book in books
        if category in book.category
    ]


def getAllBooks():
    """
    Get all books from database
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM books")

    rows = cur.fetchall()

    conn.close()

    return [row_to_book(row) for row in rows]

def exportCSV(file: str):
    """
    Write all books from the database to a csv file
    """
    books = getAllBooks()
    with open(file, "wt", encoding="utf-8") as out:
        for book in books:
            s = f"{book.ID};{book.title};{book.author};{book.date};{book.start};{book.end};"
            s += f"{", ".join(book.category)};"
            s += f"{", ".join(book.genre)};"
            s += f"{book.img}\n"
            out.write(s)
    return 

def bookExists(book_id: str) -> bool:
    """
    Check if a book (by ID) exists in the database
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT 1 FROM books WHERE ID = ? LIMIT 1",
        (book_id,)
    )

    exists = cur.fetchone() is not None

    conn.close()

    return exists         

def importCSV(file: str):
    """
    From a csv file, import books into the program and save it to the database
    """
    with open(file, "rt", encoding="utf-8") as inp:
        books = []
        for line in inp:
            book = {}
            parts = line.strip().split(";")
            book["ID"] = parts[0]
            book["title"] = parts[1]
            book["author"] = parts[2]
            book["date"] = parts[3]
            book["start"] = parts[4]
            book["end"] = parts[5]
            book["category"] = parts[6].split(",")
            book["genre"] = parts[7].split(",")
            book["img"] = parts[8]
            books.append(Book(**book))

    for book in books:
        if bookExists(book.ID) == True:
            updateBook(book)
        else:
            addBooks([book])
        
    return books



if __name__ == "__main__":
    exportCSV("book.csv")
    # importCSV("book.csv")
    # print(getAllBooks())