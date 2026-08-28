# Day 4: Tool Calling & Structured Output

## Overview

Tool calling is a powerful pattern that enables LLMs to interact with external tools and functions in a controlled, predictable manner. By combining tool calling with structured output, we create robust systems where the model suggests actions and your application executes them.

---

## What is Structured Output?

**Structured output** controls and constrains the output format returned by LLM models. Instead of getting free-form text, you receive data in a predictable, type-safe format that's easy to extract and use.

### Key Benefits:
- **Predictable Format**: Consistent data structure every time
- **Type Safety**: Guaranteed data types (strings, numbers, objects, arrays)
- **Easy Data Extraction**: No parsing or regex needed
- **Reduced Errors**: Prevents malformed responses
- **Better Integration**: Seamlessly integrates with your application code

---

## Mental Model: How Tool Calling Works

The LLM **does NOT execute functions directly**. Instead:

1. The model analyzes the user's request
2. The model generates structured arguments for the appropriate tool
3. **Your Python code** receives these arguments and executes the actual function
4. The result is returned to the model for final response generation

```
User Input
    ↓
LLM (analyzes and suggests action)
    ↓
"Call get_weather(city='Hyderabad')"
    ↓
YOUR PYTHON CODE (executes the function)
    ↓
get_weather("Hyderabad")
    ↓
Tool Result (weather data)
    ↓
LLM (processes result and responds)
    ↓
Final Response to User
```

### Key Insight:
The LLM proposes actions through structured output; your application controls execution.

---

## Common Use Cases

- **Weather APIs**: "What's the weather in Hyderabad?"
- **Database Queries**: "Find all users created last week"
- **Calculations**: "Convert 500 USD to INR"
- **Web Searches**: "Find the latest news about AI"
- **Multi-step Workflows**: Chaining multiple tool calls together

