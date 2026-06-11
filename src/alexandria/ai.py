from google import genai
from google.genai import types
from dataclasses import asdict
import alexandria.utils as u
import alexandria.data as d
import alexandria.searchGoogle as google
import alexandria.searchMoly as moly

settings = u.readSettings()

books = d.getAllBooks()

ai_settings = u.readSettings(settings["AI_settings"])

API_KEY = u.readSettings(settings["API_file"])["Gemini_API"]

SYSTEM_PROMPT = f"""
Role:
{ai_settings["system_prompt"]["role"]}

Rules:
{"\n -".join(ai_settings["system_prompt"]["rules"])}
"""

tools = []
for tool in ai_settings["tools"]:
    tools.append(types.Tool(function_declarations=[types.FunctionDeclaration(**tool)]))

client = genai.Client(api_key=API_KEY)

chat = client.chats.create(
    model=settings["Gemini_model"],
    config=types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        tools=tools
    )
)

TOOLS = {
    "addBooks": d.addBooks,
    "removeBook": d.removeBook,
    "updateBook": d.updateBook,
    "searchBy": d.searchBy,
    "searchByCategory": d.searchByCategory,
    "searchByShelf": d.searchByShelf,
    "createBookGoogle": google.createBook,
    "searchByIDGoogle": google.searchByID,
    "createBookMoly": moly.createBook,
    "searchByIDMoly": moly.searchById,
    "getAllBooks": d.getAllBooks
}

def generateResponse(user_prompt: str):
    """
    From the already set-up AI, generate a new message
    """
    response = chat.send_message(user_prompt)

    # Check if Gemini wants to call a function (or several)
    while True:

        part = response.candidates[0].content.parts[0]

        if not getattr(part, "function_call", None):
            return response.text

        call = part.function_call

        if call.name in ["removeBook", "updateBook"]:
            result = TOOLS[call.name](d.Book(**call.args))
        elif call.name == "addBooks":
            result = TOOLS[call.name]([d.Book(**b) for b in call.args["books"]])
        else:
            result = TOOLS[call.name](**call.args)

        if call.name in ["searchBy", "searchByCategory", "searchByShelf", "getAllBooks"]:
            res = []
            for r in result:
                res.append(asdict(r))
            result = res
        elif "createBook" in call.name:
            result = asdict(result)

        if result is None:
            result = {"success": True}

        tool_response = types.Part.from_function_response(
            name=call.name,
            response=result
        )

        response = chat.send_message([tool_response])

if __name__ == "__main__":

    print(f"{settings["Gemini_model"]} welcomes you! Type /exit to end chat.")

    while True:
        user_prompt = input("> ")

        if user_prompt.strip().lower() == "/exit":
            break

        try:
            response = generateResponse(user_prompt)
            print(response)
        except genai.errors.ServerError:
            print("Sorry, something went wrong. Try again later!")