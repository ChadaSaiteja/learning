import os
from dotenv import load_dotenv
import json
load_dotenv()
from google import genai

client=genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def get_weather(city):
    weather={
        "hyderabad":{
            "temperature": "30°C",
            "condition": "Sunny"
        },
        "bangalore": {
            "temperature": "28°C",
            "condition": "Cloudy"
        }
    }
    return weather.get(city.lower(), {"temperature": "N/A", "condition": "N/A"})
    
    
tool={
    "type":"function",
        "name":"get_weather",
        "description": "Get the current weather for a city",
        "parameters":{
            "type":"object",
            "properties":{
                "city":{
                    "type":"string"
                }
            },
            "required":["city"]
        }
} 

base_prompt = "Get the current weather for Hyderabad"
# base_prompt="how is the prime minister"
result= client.interactions.create(
    model="gemini-3.5-flash",
    input=base_prompt,
    tools=[tool]
)

fc_step=next((step for step in result.steps if step.type=="function_call"), None)
tool_result=None

if fc_step and fc_step.name == "get_weather":
    tool_result=get_weather(fc_step.arguments.get("city"))
    print("\nFunction call result:", tool_result)

final_result= client.interactions.create(
    model="gemini-3.5-flash",
    tools=[tool],
    previous_interaction_id=result.id,
    input=[{
            "type":"function_result",
            "name":fc_step.name,
            "call_id": fc_step.id,
            "result": [{"type": "text", "text": json.dumps(tool_result)}]
        }]
    )

    
print("\nInteraction result:", final_result.output_text)