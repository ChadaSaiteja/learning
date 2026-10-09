import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

model ="gemini-3.5-flash"


def _history_to_text(conversation_contents):
    lines = []
    for msg in conversation_contents:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        lines.append(f"{role}: {content}")
    return "\n".join(lines)


def call_google_api(conversation_contents, system_instruction):
    """Call the Google API with conversation history and system instruction."""
    prompt = _history_to_text(conversation_contents)
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(system_instruction=system_instruction),
    )
    return response.text or ""



count = 0
n = 5
history = []
summary = ""

while True:
    user_input = input("You: ")
    
    if user_input.lower() in ["exit", "quit"]:
            break
    count += 1
    if summary:
        system_instruction = "Previous conversation summary:\n" + summary
    else:
        system_instruction = "You are a helpful Chat assistant."
            
        
    history.append({"role": "user", "content": user_input})
    ai_response = call_google_api(history, system_instruction)
    print("AI: " + ai_response)
    history.append({"role": "assistant", "content": ai_response})

    if count % n == 0:
        summary_history = []
        if summary:
            summary_history.append({"role": "system", "content": "Previous summary: " + summary})
        summary_history.extend(history)
        summary = call_google_api(
            summary_history,
            "Summarize the conversation while preserving user intent, key decisions, constraints, and important facts.",
        )
        history = history[-(n * 2):]
        print("\nSummary: " + summary)




