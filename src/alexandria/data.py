from dataclasses import dataclass, asdict
import sqlite3

@dataclass
class Book:
    title: str
    author: str
    date: str
    img: str
    ID: str
    category: str
    genre: str
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

def get_connection(datafile: str = "books.db"):
    """
    Create SQL connection to datafile (books.db)
    """
    conn = sqlite3.connect(datafile)
    conn.row_factory = sqlite3.Row
    return conn

def createDatabase():
    """
    Update database format
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS books (
        title TEXT PRIMARY KEY,
        author TEXT,
        date TEXT,
        img TEXT,
        ID TEXT,
        category TEXT,
        genre TEXT,
        start TEXT,
        end TEXT
    )
    """)

    conn.commit()

    return

def addColumnToData(column_name: str, placeholder: str = "---"):
    """
    Add a new column and data to each row
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(f"ALTER TABLE books ADD COLUMN {column_name} TEXT DEFAULT '{placeholder}'")
    conn.commit()

    return

def addBooks(books: list):
    """
    Add many books to the database
    Each book need the following format:
    (title, author, date, img, id, category, genre, start, end)
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.executemany("""INSERT OR IGNORE INTO books VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", books)
    conn.commit()

    return

def updateBook(book: Book):
    """
    Update the data of one book
    """
    data = asdict(book)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    UPDATE books
    SET
        author = :author,
        date = :date,
        img = :img,
        ID = :ID,
        category = :category,
        genre = :genre,
        start = :start,
        end = :end
    WHERE title = :title
    """, data)

    conn.commit()
    conn.close()

def removeBook(book: Book):
    """
    Remove a book from the database
    """
    conn = get_connection()
    cur = conn.cursor()

def searchBy(key: str, value: str):
    """
    Search all books by a specific key, for a value

    Parameters
    ----------
    key: `str`
        Column names of data (title, author, date, img, IG, category)
    value: `str`
        Value of that column
    
    Returns
    -------
    books: `lst[Books]`
        List of each book contained in a Book class format
    """
    conn = get_connection()
    cur = conn.cursor()

    allowed_columns = {"title", "author", "date", "img", "ID", "category"}

    if key not in allowed_columns:
        raise ValueError("Invalid column name")
    
    cur.execute(f"""SELECT * FROM books WHERE {key} == ?""", (value,))

    rows = cur.fetchall()

    books = [Book(**dict(row)) for row in rows]

    return books

def getAllBooks():
    """
    Get all books from current database    
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM books")
    rows = cur.fetchall()
    return [Book(**dict(row)) for row in rows]

if __name__ == "__main__":
    # print(searchBy("category", "Reading"))
    print(getAllBooks())
    # createDatabase()
    # books = [
    #     ("A bűnbánat hegye", "Luca Tarenzi", "2025-09-15", "http://books.google.com/books/content?id=ksCGEQAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api", "ksCGEQAAQBAJ", "Reading", "Fantasy", "2026-05-17", "2026-05-21"),
    #     ("Lord of the Empty Isles", "Jules Arbeaux", "2024-06-06", "http://books.google.com/books/content?id=_PnGEAAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api", "_PnGEAAAQBAJ", "Owned", "Sci-Fi", "2025-08-20", "2025-09-05")
    # ]
    # addBooks(books)
    # book = Book("A bűnbánat hegye", "Luca Tarenzi", "2025-09-15", "http://books.google.com/books/content?id=ksCGEQAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api", "ksCGEQAAQBAJ", "Finished", "Fantasy", "2026-05-17", "2026-05-21")
    # updateBook(book)

