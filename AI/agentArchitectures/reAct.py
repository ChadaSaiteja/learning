import os
from dotenv import load_dotenv
import json
load_dotenv()
from pydantic import BaseModel, Field
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", api_key=os.getenv("GOOGLE_API_KEY"))


class SearchWebInput(BaseModel):
    query: str = Field(
        description="The topic or question to search for."
    )
    max_results: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Maximum number of search results."
    )

class CalculatorInput(BaseModel):
    a: float = Field(
        description="The first number."
    )
    b: float = Field(
        description="The second number."
    )
    operation: str = Field(
        description="The arithmetic operation to perform (add, subtract, multiply, divide)."
    )
    
    
class GetWeatherInput(BaseModel):
    city: str = Field(
        description="The city to get the weather for."
    )


@tool(args_schema=CalculatorInput)
def calculator(a: float, b: float, operation: str) -> float | str:
    """Perform basic arithmetic (add, subtract, multiply, divide) on two numbers.
    Use this for any math calculation instead of computing it yourself."""
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        return a / b
    else:
        return "Invalid operation"
    
@tool(args_schema=SearchWebInput)
def search_web(query: str, max_results: int = 5) -> str:
    """Search the web for general information, facts, or current events.
    Use this when the question needs knowledge that no other tool provides."""
    # This is a placeholder function for web search
    # In a real implementation, this would perform an actual web search
    return f"Search results for '{query}' is an subject, example 2+3 =? is arthemetic operation "


@tool(args_schema=GetWeatherInput)
def get_weather(city: str) -> dict:
    """Get the current temperature and weather condition for a city.
    Use this whenever the user asks about weather."""
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


system_prompt = "You are a helpful assistant. you will answer questions only from tools not from out side knowledge."
base_prompt = "what is maths"
# base_prompt="how is the prime minister"
llm_with_tools = llm.bind_tools([calculator, search_web, get_weather])
result = llm_with_tools.invoke([("system", system_prompt), ("human", base_prompt)])
print("initial content:", result.content)
# print("initial tool_calls:", result.tool_calls)
while result.tool_calls:
    print("result while loop:", result)
    tool_calls = result.tool_calls

    tool_to_call = tool_calls[0]
    print("tool_to_call:", tool_to_call)
    
    tool_name = tool_to_call["name"]
    tool_args = tool_to_call["args"]
    print("tool_name:", tool_name)
    print("tool_args:", tool_args)
    
    # Here you would call the actual tool with the arguments
    if tool_name == "calculator":
        tool_result = calculator.invoke(tool_args)
    elif tool_name == "search_web":
        tool_result = search_web.invoke(tool_args)
    elif tool_name == "get_weather":
        tool_result = get_weather.invoke(tool_args)
    else:
        tool_result = f"Unknown tool: {tool_name}"
    
    print("tool_result:", tool_result)
    
    # Update the base prompt with the tool result for the next iteration
    base_prompt += f"\nTool result for {tool_name}: {tool_result}"
    
    result = llm_with_tools.invoke([("system", system_prompt), ("human", base_prompt)])
    print("content:", result.content)
    print("tool_calls:", result.tool_calls)
# The model doesn't run tools itself - it returns which tool to call and with what args
print("content:", result.content)
print("tool_calls:", result.tool_calls)