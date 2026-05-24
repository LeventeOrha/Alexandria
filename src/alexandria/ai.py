from google import genai
from google.genai import types
import Alexandria.src.alexandria.utils as u
import Alexandria.src.alexandria.data as d
import Alexandria.src.alexandria.search as s

settings = u.readSettings()

books = d.getAllBooks()

SYSTEM_PROMPT = f"""
You are an AI librarian, helping the user pick their next book and manage their collection.

ONLY recomment books from this list:
{books}

Rules:
- You may use the searchByID tool to retrieve full book data when needed.
- Do NOT invent books
- ONLY use books from the provided list
- Remember previous conversation context
- If nothing matched, say so
"""

client = genai.Client(api_key=settings["Gemini_API"])

search_tool = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="searchByID",
            description="Retrieve full book data using its ID from the internal database.",
            parameters={
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "The unique book ID"
                    }
                },
                "required": ["id"]
            },
        )
    ]
)

chat = client.chats.create(
    model=settings["Gemini_model"],
    config=types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        tools=[search_tool]
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