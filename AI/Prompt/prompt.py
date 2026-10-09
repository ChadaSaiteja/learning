import os
from dotenv import load_dotenv
load_dotenv()
from google import genai
print("GOOGLE_API_KEY:", os.getenv("GOOGLE_API_KEY"))
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))



base_prompt = "Explain how machine learning works and its applications"

prompt_simple = "What is machine learning? Explain it in simple words that a 10-year-old can understand."

prompt_technical = "Provide a detailed technical explanation of supervised learning, unsupervised learning, and reinforcement learning with mathematical foundations and algorithmic complexity analysis."

prompt_business = "How can organizations implement machine learning to improve business outcomes? Include real-world examples and ROI considerations."


interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input=base_prompt
)
print(interaction.output_text)