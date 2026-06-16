import yaml
import os
import json
import traceback
from google import genai
from dataclasses import asdict, fields
import alexandria.utils as u
import alexandria.categories as transl
from alexandria.ai import AI
from alexandria.data import Database, Book
from alexandria.searchGoogle import Google
from alexandria.searchMoly import Moly

class CMD:
    def __init__(self, params: dict):
        """
        Create a new Command Line operating book diary
        Also setting up things if newly installed (first run, database does not exist)
        """
        self.db = Database(params["datafile"])
        self.moly = Moly(self.db)

        # If everything is new, force to set a language
        self.text = self.readYML(params["Language_file"])
        while self.db.is_new:
            if params["Language"] in list(self.text):
                break
            params["Language"] = input("Select language: 'en', 'hu': ")

        self.lang = params["Language"]
        self.text = self.text[params["Language"]]

        # If there is no API key file, create it and write it out
        if not os.path.exists(params["API_file"]):
            if input(self.text["APIFileNotFound"]).lower().strip() in ["y", "i"]:
                with open(params["API_file"], "wt", encoding="utf-8") as out:
                    API_keys = {}
                    API_keys["GB_API"] = input(self.text["GoogleBooksAPI"]).strip()
                    API_keys["Gemini_API"] = input(self.text["GeminiAPI"]).strip()
                    json.dump(API_keys, out, ensure_ascii=False, indent=4)
            else:
                exit()

        API_keys = u.readSettings(params["API_file"])
        ai_settings = u.readSettings(params["AI_settings"])

        self.google = Google(API_keys["GB_API"])
        self.ai = AI(API_keys, params["Gemini_model"], ai_settings, self.db)

        if self.db.is_new:
            u.writeSettings(params)

    def readYML(self, file: str) -> dict:
        """
        Reading a .yml/.yaml file
        """
        with open(file, 'rt', encoding="utf-8") as inp:
            text = yaml.safe_load(inp)
        return text
    
    def searchNew(self):
        """
        Do a new search of book, based on its title and author
        Option to change language, as hu defaults to using to moly.hu
        Other languagues are searched on Google Books
        """
        if input(self.text["NewSearchDefLang"].replace("%", self.lang)) == "n":
            new_lang = input(self.text["NewLangCode"])
        else:
            new_lang = self.lang

        title = input(self.text["Title"])
        author = input(self.text["Author"])

        if new_lang == "hu":
            books = self.moly.searchBook(title, author)
            for i in range(len(books)):
                print(f"{i+1}) {books[i]["title"]} - {books[i]["author"]} ({books[i]["date"]})")
                for j in range(len(books[i]["imgs"])):
                    letter = chr(ord('a') + j)
                    print(f"\t{letter}) {books[i]["imgs"][j]}")
            
            pick = input(self.text["PickBook"])

            if pick == "c" or len(pick) == 0:
                return
            
            book = books[int(pick[0]) - 1]
            img_idx = ord(pick[1]) - ord('a')

            shelf = input(self.text["PickShelf"])
            if input(self.text["PickDate"]) in ["i", "y"]:
                start = input(self.text["EnterStartingDate"])
                end = input(self.text["EnterEndingDate"])
            else:
                start = "---"
                end = "---"

            book = self.moly.createBook(book["ID"], shelf, img_idx, start, end)

        else:
            books = self.google.searchBook(title, author, new_lang)

            for i in range(len(books)):
                print(f"{i+1}) {books[i]["title"]} - {books[i]["author"]} ({books[i]["date"]}) - {books[i]["img"]}")
            
            pick = input(self.text["PickBook"])

            if pick == "c" or len(pick) == 0:
                return
            
            book = books[int(pick) - 1]

            shelf = input(self.text["PickShelf"])
            if input(self.text["PickDate"]) in ["i", "y"]:
                start = input(self.text["EnterStartingDate"])
                end = input(self.text["EnterEndingDate"])
            else:
                start = "---"
                end = "---"

            book = self.google.createBook(book["ID"], shelf, start, end)

        self.db.addBooks([book])
        print(self.text["SuccessfulSaveShelf"].replace("%", shelf))
        return
    
    def listBooks(self, books: list[Book]):
        """
        List out all books from `books`, their title and author
        Waiting for user to pick one book from them
        Then listing out all details of that book
        Prompting if they want to change anything in it
        """
        for i, book in enumerate(books):
            print(f"{i+1}) {book.title} - {book.author}")
        pick = input(self.text["ListBookDetails"])

        if pick == "c" or len(pick) == 0:
            return

        book = books[int(pick) - 1]
        book = asdict(book)

        if "moly.hu" in book["ID"]:
            all_data = self.moly.searchByID(book["ID"])
            book["abstract"] = all_data["abs"]
        
        else:
            all_data = self.google.searchByID(book["ID"])
            book["abstract"] = all_data["volumeInfo"]["description"]

        print(f"{book['title']} - {book['author']}")
        print(book['img'])
        print()
        print(f"{self.text['Abstract']}:")
        print(book["abstract"])
        print()
        print(f"{self.text["Categories"]}: {", ".join(book["category"])}")
        print(f"{self.text["Shelves"]}: {", ".join(book["shelf"])}")
        print(f"{self.text["StartingDate"]} {book["start"]}")
        print(f"{self.text["EndDate"]} {book["end"]}")

        change = input(self.text["ModifyBook"]).strip()

        # Option to change the data
        if change == "m":
            while True:
                key = input(self.text["PropertyToModify"])
                key = transl.translateProperty(key, self.lang)

                allowed = {f.name for f in fields(Book)}

                if key in allowed:
                    break
                print(self.text["NoSuchProperty"])

            value = input(self.text["PropertyValue"])
            book[key] = value

            # Unpacking the dictionary into a Book class
            b = {
                "title": book["title"],
                "author": book["author"],
                "date": book["date"],
                "img": book["img"],
                "ID": book["ID"],
                "shelf": book["shelf"] if type(book["shelf"]) is list else book["shelf"].replace(" ", "").split(","),
                "category": book["category"] if type(book["category"]) is list else book["category"].replace(" ", "").split(","),
                "start": book["start"],
                "end": book["end"]
            }

            book = Book(**b)

            self.db.updateBook(book)

            print(self.text["SuccessfulSave"])
        
        elif change == "d":
            if input(self.text["DeleteEnsuring"]) in ["y", "i"]:
                self.db.removeBook(book["ID"])
                print(self.text["DeleteSuccess"])

        return

    def listShelf(self):
        """
        Search book on a specific shelf
        """
        shelf = input(self.text["PickShelf"])
        books = self.db.searchByShelf(shelf)

        if len(books) == 0:
            print(self.text["NoSuchBookShelf"].replace("%", shelf))
            return
        
        self.listBooks(books)
        return

    def searchInLibrary(self):
        """
        Search in the whole library, by any key-value pair
        """
        key = input(self.text["SearchByKey"])
        value = input(self.text["SearchByValue"])

        key = transl.translateProperty(key, self.lang)

        books = self.db.searchBy(key, value)

        if len(books) == 0:
            print(self.text["NoSuchBook"])
            return
        
        self.listBooks(books)
        return

    def talkWithAI(self):
        """
        Talk with AI assistant
        """
        print(self.text["AiWelcome"])

        while True:
            user_prompt = input("> ")

            if user_prompt.strip().lower() == "/exit":
                print(self.text["AiGoodBye"])
                break

            if user_prompt.strip().lower() == "/help":
                print(self.text["AiHelp"])
                continue

            if "/save" in user_prompt.strip().lower():
                self.ai.saveChat(user_prompt.split(" ")[1])
                continue

            try:
                response = self.ai.generateResponse(user_prompt)
                print(response)
            except genai.errors.ServerError:
                print(self.text["AiError"])
                if input(self.text["AiSaveChat"]) in ["y", "i"]:
                    self.ai.saveChat("gemini_chat_log.yaml")
                break
            except Exception as e:
                print("Something else went wrong. Check the error please!")
                if input("Do you want to save the chat log? (y/n) ") == "y":
                    self.ai.saveChat("gemini_chat_log.yaml")
                print(e.__repr__())
                traceback.print_exc()
                break

    def settings(self):
        """
        Display current settings and change them
        """
        params = u.readSettings()
        print(self.text["SettingsOptions"].replace("%", params["Language"], 1).replace("%", params["Gemini_model"]))
        pick = input(self.text["SettingsOptionsChoose"])

        try:
            pick = int(pick)
        except:
            print(self.text["NoSuchOption"])
            return
        if 0 < pick < 6:
            if pick == 1:
                self.lang = input(self.text["ChooseLanguage"])
                params["Language"] = self.lang
            elif pick == 2:
                ai_model = input(self.text["AiModelChange"])
                params["Gemini_model"] = ai_model
            elif pick == 3:
                params["GUI_useage"] = True
            elif pick == 4:
                file = input(self.text["ExportFilename"]).strip()
                if "csv" in file:
                    self.db.exportCSV(file)
                else:
                    self.db.exportYML(file)
            elif pick == 5:
                while True:
                    file = input(self.text["ImportFilename"]).strip()
                    if os.path.exists(file):
                        break
                    print(self.text["FileNotFound"])
                try:
                    self.db.importCSV(file)
                    print(self.text["SuccessfulImport"])
                except:
                    print(self.text["ImportError"]) 
            u.writeSettings(params)
            return
        print(self.text["NoSuchOption"])
        return
 
    def main(self):
        """
        Main loop, handles main options and exit
        """
        print(self.text["WelcomeText"])
        while True:
            print(self.text["Options"])
            try:
                answer = int(input(self.text["OptionChoose"]))
            except ValueError:
                print(self.text["NoSuchOption"])
                continue

            if answer == 1:
                self.searchNew()
            elif answer == 2:
                self.listShelf()
            elif answer == 3:
                self.searchInLibrary()
            elif answer == 4:
                self.talkWithAI()
            elif answer == 5:
                self.settings()
            elif answer == 6:
                print(self.text["Exit"])
                break
            else:
                print(self.text["NoSuchOption"])

        self.db.close()