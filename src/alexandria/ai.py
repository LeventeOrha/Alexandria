from google import genai
from google.genai import types
from dataclasses import asdict
import yaml
from alexandria.data import Book, Database
from alexandria.searchGoogle import Google
from alexandria.searchMoly import Moly

class AI:
    def __init__(self, API_keys: dict, model: str, settings: dict, db: Database):
        self.API_KEY = API_keys["Gemini_API"]
        self.settings = settings
        self.model = model
        self.moly = Moly(db)
        self.google = Google(API_keys["GB_API"])
        self.db = db

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
            "searchBy": self.db.searchBy,
            "searchByCategory": self.db.searchByCategory,
            "searchByShelf": self.db.searchByShelf,
            "createBookGoogle": self.google.createBook,
            "searchByIDGoogle": self.google.searchByID,
            "createBookMoly": self.moly.createBook,
            "searchByIDMoly": self.moly.searchByID,
            "getAllBooks": db.getAllBooks
        }

    def saveChat(self, filename: str):
        """
        Save the conversation
        """
        with open(filename, "wt", encoding="utf-8") as out:
            yaml.safe_dump(self.conversation_log, out, sort_keys=False, allow_unicode=True)
        return {"success": True}


    def generateResponse(self, user_prompt: str):
        """
        Generate a new message
        """
        response = self.chat.send_message(user_prompt)

        self.conversation_log.append({"role": "user", "content": user_prompt})

        # Check out if Gemini wants to call a function (or several)
        while True:

            part = response.candidates[0].content.parts[0]

            if not getattr(part, "function_call", None):
                self.conversation_log.append({"role": "assistant", "content": response.text})
                return response.text

            call = part.function_call

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

            self.conversation_log.append({"role": "tool call", "name": call.name, "args": dict(call.args), "response": result})

            tool_response = types.Part.from_function_response(
                name=call.name,
                response=result
            )

            response = self.chat.send_message([tool_response])

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