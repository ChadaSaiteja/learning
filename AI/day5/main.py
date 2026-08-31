from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio
import os
from dotenv import load_dotenv
import json
load_dotenv()
from google import genai

client=genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI()


async def chat_with_ai(prompt):
    
    stream=client.interactions.create(
        model='gemini-3.5-flash',
        input=prompt,
        stream=True
    )
    for event in stream:
        await asyncio.sleep(2)
        if event.event_type == "step.start":
            yield f"\n--- Step: {event.step.type} ---"
        elif event.event_type == "step.delta":
            if event.delta.type == "text":
                yield event.delta.text
            elif event.delta.type == "thought_summary":
                if event.delta.content.type == "text":
                    yield event.delta.content.text
        elif event.event_type == "interaction.completed":
            yield f"\n\nTotal Tokens: {event.interaction.usage.total_tokens}"


async def generate_data():
    words = ["item1", "item2", "item3"]
    for word in words:
        yield word
        await asyncio.sleep(1)
    

@app.get("/stream")
async def stream():
    return StreamingResponse(generate_data(), media_type="text/plain")

@app.get("/chat")
async def chat():
    return StreamingResponse(chat_with_ai("explain about ai in 100 words"), media_type="text/plain")