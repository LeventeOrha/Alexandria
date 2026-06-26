from dataclasses import dataclass, asdict
from typing import List
import sqlite3
import json
import os

# Book class to hold everything together
@dataclass
class Book:
    title: str
    author: str
    date: str
    img: str
    ID: str
    shelf: List[str]
    category: List[str]
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
        s += f"\tshelf: {self.shelf}\n"
        s += f"\tcategory: {self.category}\n"
        s += f"\tstart: {self.start}\n"
        s += f"\tend: {self.end}\n"
        return s
    
# Database class, to not open connection again and again
class Database:

    def __init__(self, datafile: str):
        self.is_new = not os.path.exists(datafile)

        self.filename = datafile
        self.conn = sqlite3.connect(datafile)
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()

        # If the database didn't exist yet, create a new
        if self.is_new:
            self.createDatabase()

    def createDatabase(self):
        """
        Create an empty database with these keys
        """
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS books (
            ID TEXT PRIMARY KEY,
            title TEXT,
            author TEXT,
            date TEXT,
            img TEXT,
            shelf TEXT,
            category TEXT,
            start TEXT,
            end TEXT
        )
        """)
        self.conn.commit()
        return {"success": True}
    
    def close(self):
        """
        Close the connection
        """
        self.conn.close()
        return {"success": True}
    
    def rowToBook(self, row):
        """
        Convert SQLite row to Book object
        """
        data = dict(row)

        data["shelf"] = json.loads(data["shelf"])
        data["category"] = json.loads(data["category"])

        return Book(**data)
    
    def addBooks(self, books: list[Book]):
        """
        Add many books to the database
        """
        data = []
        for book in books:
            data.append((book.ID, book.title, book.author, book.date, book.img,
                         json.dumps(book.shelf), json.dumps(book.category), book.start, book.end))
            
        self.cur.executemany("""
        INSERT OR IGNORE INTO books
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, data)

        self.conn.commit()
        return {"success": True}
    
    def updateBook(self, book: Book):
        """
        Update data of one book, based on ID
        """
        data = asdict(book)
        data["shelf"] = json.dumps(book.shelf)
        data["category"] = json.dumps(book.category)

        self.cur.execute("""
        UPDATE books
        SET
            title = :title,
            author = :author,
            date = :date,
            img = :img,
            shelf = :shelf,
            category = :category,
            start = :start,
            end = :end
        WHERE ID = :ID
        """, data)

        self.conn.commit()
        return {"success": True}
    
    def removeBook(self, ID: str):
        """
        Remove book with given ID
        """
        self.cur.execute("""
        DELETE FROM books
        WHERE ID = ?
        """, (ID,))

        self.conn.commit()
        return {"success": True}
    
    def searchBy(self, key: str, value: str) -> list[Book]:
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
        allowed_columns = [
            "ID", "title", "author", "date",
            "img", "start", "end", "category", "shelf"
        ]

        if key == "category":
            books = self.searchByCategory(value)
            return books
        elif key == "shelf":
            books = self.searchByShelf(value)
            return books

        if key not in allowed_columns:
            raise ValueError(f"Invalid column name - {key}")
        
        self.cur.execute(
            f"SELECT * FROM books WHERE LOWER({key}) LIKE LOWER(?)",
            (f"%{value}%",)
        )

        rows = self.cur.fetchall()

        return [self.rowToBook(row) for row in rows]

    def getAllBooks(self) -> list[Book]:
        """
        Get all books from the database
        """
        self.cur.execute("SELECT * FROM books")

        rows = self.cur.fetchall()

        return [self.rowToBook(row) for row in rows]
    
    def searchByCategory(self, category: str) -> list[Book]:
        """
        Search books by a category
        """
        books = self.getAllBooks()

        res = []
        for book in books:
            if category in book.category:
                res.append(book)
        
        return res
    
    def searchByShelf(self, shelf: str) -> list[Book]:
        """
        Search books by a shelf
        """
        books = self.getAllBooks()

        res = []
        for book in books:
            if shelf in book.shelf:
                res.append(book)
        
        return res
    
    def getShelves(self):
        """
        List out all available shelves
        """
        books = self.getAllBooks()
        shelves = []
        for book in books:
            for shelf in book.shelf:
                if shelf not in shelves:
                    shelves.append(shelf)

        return shelves
    
    def exportCSV(self, filename: str):
        """
        Write all books from the database to a csv file
        """
        books =self.getAllBooks()
        with open(filename, "wt", encoding="utf-8") as out:
            for book in books:
                s = f"{book.ID};{book.title};{book.author};{book.date};{book.start};{book.end};"
                s += f"{", ".join(book.shelf)};"
                s += f"{", ".join(book.category)};"
                s += f"{book.img}\n"
                out.write(s)
        return {"success": True}
    
    def exportYML(self, filename: str):
        """
        Write all books from the database to a YAML file (readibilty, debugging)
        """
        import yaml
        books = self.getAllBooks()
        with open(filename, "wt", encoding="utf-8") as out:
            yaml.safe_dump([asdict(book) for book in books], out, sort_keys=False, allow_unicode=True)
        return {"success": True}
    
    def bookExists(self, ID: str) -> bool:
        """
        Check if book with ID exists
        """
        self.cur.execute("SELECT 1 FROM books WHERE ID = ? LIMIT 1", (ID,))
        exists = self.cur.fetchone() is not None
        return exists
    
    def importCSV(self, filename: str):
        """
        From a csv file, import books into the database
        Update them if existing, adding if ID not exist
        """
        with open(filename, "rt", encoding="utf-8") as inp:
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
                book["shelf"] = parts[6].split(", ")
                book["category"] = parts[7].split(", ")
                book["img"] = parts[8]
                books.append(Book(**book))

        new_books = []
        for book in books:
            if self.bookExists(book.ID):
                self.updateBook(book)
            else:
                new_books.append(book)
        self.addBooks(new_books)
            
        return books
    
if __name__ == "__main__":
    db = Database("../../datafiles/books.db")
    db.exportYML("books.yaml")
    db.close()