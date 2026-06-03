from google import genai
from google.genai import types
import alexandria.utils as u
import alexandria.data as d
import alexandria.search as s

settings = u.readSettings()

books = d.getAllBooks()

ai_settings = u.readSettings(settings["AI_settings"])

SYSTEM_PROMPT = f"""
Role:
{ai_settings["system_prompt"]["role"]}

Rules:
{"\n -".join(ai_settings["system_prompt"]["rules"])}

{ai_settings["system_prompt"]["conditions"][0]}
{books}
"""

tools = []
for tool in ai_settings["tools"]:
    tools.append(types.Tool(function_declarations=[types.FunctionDeclaration(**tool)]))

client = genai.Client(api_key=settings["Gemini_API"])

chat = client.chats.create(
    model=settings["Gemini_model"],
    config=types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        tools=tools
    )
)

print(f"{settings["Gemini_model"]} welcomes you! Type /exit to end chat.")

while True:
    user_prompt = input("> ")

    if user_prompt.strip().lower() == "/exit":
        break

    response = chat.send_message(user_prompt)

    # Check if Gemini wants to call a function
    if response.candidates[0].content.parts[0].function_call:
        call = response.candidates[0].content.parts[0].function_call

        if call.name == "searchByID":
            book_id = call.args["id"]

            result = s.searchByID(book_id)  # your function

            tool_response = types.Part.from_function_response(
                name="searchByID",
                response=result  # your dictionary is fine here
            )

            response = chat.send_message([tool_response])

    print(response.text)