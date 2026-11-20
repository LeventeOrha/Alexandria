from google import genai
from google.genai import types
from dataclasses import asdict
import yaml
from alexandria.data import Book, Database
from alexandria.searchGoogle import Google
from alexandria.searchMoly import Moly

class AI:
    def __init__(self, API_keys: dict, model: str, daily_limit: int, settings: dict, db: Database):
        self.API_KEY = API_keys["Gemini_API"]
        self.settings = settings
        self.daily_limit = daily_limit
        self.model = model
        self.moly = Moly(db)
        self.google = Google(API_keys["GB_API"], db)
        self.db = db
        self.n_requests = 0 # Number of sent requests

        self.system_prompt = f"Role: \n{self.settings["system_prompt"]["role"]}\n"
        self.system_prompt += f"Rules: \n{"\n -".join(self.settings["system_prompt"]["rules"])}"

        tools = []

        for tool in self.settings["tools"]:
            tools.append(types.Tool(function_declarations=[types.FunctionDeclaration(**tool)]))

        self.client = genai.Client(api_key=self.API_KEY)

        self.chat = self.client.chats.create(
            model = self.model,
            config = types.GenerateContentConfig(
                system_instruction = self.system_prompt,
                tools = tools
            )
        )

        self.conversation_log = []

        self.tools = {
            "addBooks": self.db.addBooks,
            "removeBook": self.db.removeBook,
            "updateBook": self.db.updateBook,
            "createBook": self.createBook,
            "searchBy": self.db.searchBy,
            "searchByCategory": self.db.searchByCategory,
            "searchByShelf": self.db.searchByShelf,
            "createBookGoogle": self.google.createBook,
            "searchByIDGoogle": self.google.searchByID,
            "createBookMoly": self.moly.createBook,
            "searchByIDMoly": self.moly.searchByID,
            "getAllBooks": db.getAllBooks
        }

    def createBook(
        self,
        ID: str,
        title: str,
        author: str,
        date: str,
        img: str,
        shelf: list[str],
        category: list[str],
        color: str = "#FFFFFF",
        start: str = "---",
        end: str = "---"
    ) -> Book:
        """Create a Book instance from details supplied by the user."""
        return Book(
            ID=ID,
            title=title,
            author=author,
            date=date,
            img=img,
            shelf=shelf,
            category=category,
            color=color,
            start=start,
            end=end
        )

    def saveChat(self, filename: str):
        """
        Save the conversation
        """
        with open(filename, "wt", encoding="utf-8") as out:
            yaml.safe_dump(self.conversation_log, out, sort_keys=False, allow_unicode=True)
        return {"success": True}

    def _send(self, content):
        if self.n_requests >= self.daily_limit:
            raise RuntimeError("Daily Gemini limit reached")
        self.n_requests += 1
        return self.chat.send_message(content)

    def generateResponse(self, user_prompt: str):
        """
        Generate a new message
        """
        response = self._send(user_prompt)

        self.conversation_log.append({"role": "user", "content": user_prompt})

        # Check out if Gemini wants to call a function (or several)
        assistant_text = []
        while True:
            tool_responses = []

            for part in response.candidates[0].content.parts:
                call = getattr(part, "function_call", None)
                if call:
                    try:
                        if call.name in ["removeBook", "updateBook"]:
                            result = self.tools[call.name](Book(**call.args))
                        elif call.name == "addBooks":
                            result = self.tools[call.name]([Book(**b) for b in call.args["books"]])
                        else:
                            result = self.tools[call.name](**call.args)

                        if call.name in ["searchBy", "searchByCategory", "searchByShelf", "getAllBooks"]:
                            result = {"books": [asdict(r) for r in result]}
                        elif "createBook" in call.name:
                            result = asdict(result)

                        if result is None:
                            result = {"success": True}
                    except Exception as error:
                        error_message = str(error)
                        for secret in (self.API_KEY, self.google.API_key):
                            if secret:
                                error_message = error_message.replace(secret, "[REDACTED]")
                        result = {
                            "success": False,
                            "error": {
                                "type": type(error).__name__,
                                "message": error_message
                            }
                        }

                    self.conversation_log.append({"role": "tool call", "name": call.name, "args": dict(call.args), "response": result})
                    tool_responses.append(types.Part.from_function_response(
                        name=call.name,
                        response=result
                    ))
                else:
                    text = getattr(part, "text", None)
                    if text:
                        assistant_text.append(text)

            if tool_responses:
                response = self._send(tool_responses)
                continue

            response_text = "".join(assistant_text)
            self.conversation_log.append({"role": "assistant", "content": response_text})
            return response_text

if __name__ == "__main__":
    import traceback
    import alexandria.utils as u
    params = u.readSettings()
    API_keys = u.readSettings(params["API_file"])
    ai_settings = u.readSettings(params["AI_settings"])
    db = Database(params["datafile"])
    gemini = AI(API_keys, params["Gemini_model"], ai_settings, db)

    print("Welcome! Type /help to display guide.")

    while True:
        user_prompt = input("> ")

        if user_prompt.strip().lower() == "/exit":
            print("We had a nice chat! Good bye!")
            break

        if user_prompt.strip().lower() == "/help":
            print("Help requested. Here are the commands you may use: ")
            print("- /help - Display this guide")
            print("- /exit - End chat and close AI assistant")
            print("- /save <filename> - Save conversation into 'filename'")
            continue

        if "/save" in user_prompt.strip().lower():
            gemini.saveChat(user_prompt.split(" ")[1])
            continue
        
        try:
            response = gemini.generateResponse(user_prompt)
            print(response)
        except genai.errors.ServerError:
            print("Sorry, I don't feel like it today. Come back tomorrow!")
            if input("Do you want to save the chat log? (y/n) ") == "y":
                gemini.saveChat("gemini_chat_log.yaml")
            break
        except Exception as e:
            print("Something else went wrong. Check the error please!")
            if input("Do you want to save the chat log? (y/n) ") == "y":
                gemini.saveChat("gemini_chat_log.yaml")
            print(e.__repr__())
            traceback.print_exc()
            break