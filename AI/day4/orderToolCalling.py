import os
from dotenv import load_dotenv
import json
load_dotenv()
from google import genai
client=genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

model='gemini-3.5-flash'

def get_order_details(order_id):
    orders = {
        "ord-123": {
            "addressId": "add-123",
        },
        "ord-456": {
            "addressId": "add-456",
        }
    }
    return orders.get(order_id, {"addressId": "N/A"})

def get_available_slots(address_id):
    slots = {
        "add-123": ["2024-06-10 10:00", "2024-06-10 14:00"],
        "add-456": ["2024-06-11 09:00", "2024-06-11 13:00"]
    }
    return slots.get(address_id, ["N/A"])


def get_order_status(order_id):
    orders = {
        "ord-123": {
            "status": "installation scheduled",
          
        },
        "ord-456": {
            "status": "installation pending",
        }
    }
    return orders.get(order_id, {"status": "N/A"})

tools=[
    {
        "type": "function",
        "name": "get_order_details",
        "description": "Retrieve details of an order by its ID",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {"type": "string"}
            },  
            "required": ["order_id"]    
        }
    },    
    {
        "type": "function",
        "name": "get_available_slots",
        "description": "Retrieve available slots for a given address ID",
        "parameters": {
            "type": "object",
            "properties": {
                "address_id": {"type": "string"}
            },
            "required": ["address_id"]
        }
    },
    {
        "type": "function",
        "name": "get_order_status",
        "description": "Retrieve the status of an order by its ID",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {"type": "string"}
            },
            "required": ["order_id"]
        }
    }
]



def call_google_api(input_prompt, tools, previous_interaction=None, fc_step=None, tool_result=None):
    """
    Call the Google API with tool support.
    Handles both initial requests and tool result follow-ups.
    """
    payload = {
        "model": model,
        "input": input_prompt,
        "tools": tools
    }
    
    if previous_interaction:
        payload["previous_interaction_id"] = previous_interaction.id

    if tool_result and fc_step:
        payload["input"] = [{
            "type": "function_result", 
            "name": fc_step.name, 
            "call_id": fc_step.id,
            "result": [{"type": "text", "text": json.dumps(tool_result)}] 
        }]
    
    return client.interactions.create(**payload)


# Main execution loop
input_prompt = input("Enter your prompt: ")
interaction = call_google_api(input_prompt, tools)

while True:
    fc_step = next((step for step in interaction.steps if step.type == "function_call"), None)
    
    if not fc_step:
        print("\nFinal Response:")
        print(interaction.output_text)
        break
    
    print(f"\n🔧 Executing function: {fc_step.name}")
    print(f"   Arguments: {fc_step.arguments}")
    
    tool_result = None
    if fc_step.name == "get_order_details":
        tool_result = get_order_details(fc_step.arguments.get("order_id"))
    elif fc_step.name == "get_available_slots":
        tool_result = get_available_slots(fc_step.arguments.get("address_id"))
    elif fc_step.name == "get_order_status":
        tool_result = get_order_status(fc_step.arguments.get("order_id"))
    
    print(f"   Result: {tool_result}\n")
    
    interaction = call_google_api("", tools, interaction, fc_step, tool_result)