# Day 3: Prompting Techniques

## What is Prompting?

Prompting is a process of writing clear instructions to an AI model so that it generates responses that meet your requirements.

---

## Types of Prompting

### 1. Short Prompting

#### Zero-Shot Prompting
- You instruct the model to perform a task without providing any examples
- The model relies on its pre-trained knowledge to complete the task
- Best for straightforward questions that don't require context

#### One-Shot Prompting
- You provide **1 example** in your prompt along with the instruction
- The model learns from this single example to understand the expected output format
- Useful when you need to show a specific pattern

#### Few-Shot Prompting
- You provide **multiple examples** (2-5) in the prompt
- Also known as **in-context learning**
- The examples guide the model to produce the expected result
- Very effective for specific tasks and desired output formats

---

### 2. Chain of Thought Prompting

- A technique that combines few-shot prompting with step-by-step reasoning
- You ask the LLM to explain its thinking process step by step
- You provide examples that demonstrate this reasoning pattern
- Particularly effective for handling complex logic and mathematical problems

---

### 3. Prompt Chaining

- A technique where you break down complex tasks into multiple sequential prompts
- The output from one prompt becomes the input for the next
- Useful for achieving more sophisticated results through a series of guided steps

to break complex task into subtask, then one subtask response is used for other prompt.



ReAct:

acting and reasoning
