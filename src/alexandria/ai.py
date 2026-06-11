from google import genai
from google.genai import types
from dataclasses import asdict
import alexandria.utils as u
import alexandria.data as d
import alexandria.searchGoogle as Google
import alexandria.searchMoly as Moly

class AI:
    def __init__(self, API_file: str, model: str, settings_file: str):
        self.API_KEY = u.readSettings(API_file)["Gemini_API"]
        self.settings = u.readSettings(settings_file)
        self.model = model

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

        self.tools = {
            "addBooks": d.addBooks,
            "removeBook": d.removeBook,
            "updateBook": d.updateBook,
            "searchBy": d.searchBy,
            "searchByCategory": d.searchByCategory,
            "searchByShelf": d.searchByShelf,
            "createBookGoogle": Google.createBook,
            "searchByIDGoogle": Google.searchByID,
            "createBookMoly": Moly.createBook,
            "searchByIDMoly": Moly.searchById,
            "getAllBooks": d.getAllBooks
        }

    def generateResponse(self, user_prompt: str):
        """
        Generate a new message
        """
        response = self.chat.send_message(user_prompt)

        # Check out if Gemini want to call a function (or several)
        while True:

            part = response.candidates[0].content.parts[0]

            if not getattr(part, "function_call", None):
                return response.text

            call = part.function_call

            if call.name in ["removeBook", "updateBook"]:
                result = self.tools[call.name](d.Book(**call.args))
            elif call.name == "addBooks":
                result = self.tools[call.name]([d.Book(**b) for b in call.args["books"]])
            else:
                result = self.tools[call.name](**call.args)

            if call.name in ["searchBy", "searchByCategory", "searchByShelf", "getAllBooks"]:
                result = {"books": [asdict(r) for r in result]}
                
            elif "createBook" in call.name:
                result = asdict(result)

            if result is None:
                result = {"success": True}

            tool_response = types.Part.from_function_response(
                name=call.name,
                response=result
            )

            response = self.chat.send_message([tool_response])

if __name__ == "__main__":
    params = u.readSettings()
    gemini = AI(params["API_file"], params["Gemini_model"], params["AI_settings"])

    print("Welcome! Type /exit to end chat.")

    while True:
        user_prompt = input("> ")

        if user_prompt.strip().lower() == "/exit":
            print("We had a nice chat! Good bye!")
            break
        
        try:
            response = gemini.generateResponse(user_prompt)
            print(response)
        except genai.errors.ServerError:
            print("Sorry, I don't feel like it today. Come back tomorrow!")
            break