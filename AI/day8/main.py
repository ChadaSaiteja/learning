import os
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field
from typing import Literal, List
from fastapi import FastAPI
from google.genai import types

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise RuntimeError("GOOGLE_API_KEY is not set")

client = genai.Client(api_key=api_key)
model ="gemini-3.5-flash"


class StructuredSummary(BaseModel):
    summary: str = Field(description="The structured summary of the article.")
    key_points: List[str] = Field( description="The key points extracted from the article.")
    sentiment: Literal["positive", "negative", "neutral"] = Field(description="The overall sentiment of the article.")
    
async def call_google_api(article_text: str):
    try:
        """Call the Google API with conversation history and system instruction."""
        response_stream = client.models.generate_content_stream(
            model=model,
            contents=article_text,
            config=types.GenerateContentConfig(
                    system_instruction="You are an expert editorial assistant. Analyze the user's article text and extract a structured summary.",
                    response_mime_type="application/json",
                    response_schema=StructuredSummary
                )
        )
        print("Calling Google API with article text:", article_text)
        print("Received response from Google API.")
        for chunk in response_stream:
            if chunk.text:
                print("Yielding chunk:", chunk.text)
                yield chunk.text
        
    except Exception as e:
        print(f"Error calling Google API: {e}")
 
 
 
 
 
app = FastAPI()

@app.get("/structured-summary/")
async def get_structured_summary(conversation_contents: str):
    print("Received request for structured summary.")
    
    conversation_contents =  """For the alternative investment firm, see Blackstone Inc. For other uses, see Black Rock (disambiguation).
BlackRock, Inc.


Headquarters at 50 Hudson Yards
Type	Public
Traded as	
NYSE: BLK
S&P 100 component
S&P 500 component
ISIN	US450614482
Industry	Investment management
Founded	March 9, 1988; 38 years ago
Founders	
Robert S. Kapito
Larry Fink
Susan Wagner
Headquarters	50 Hudson Yards, New York City, U.S.
Area served	Worldwide
Key people	
Larry Fink
(chairman and CEO)
Robert S. Kapito
(president)
Philipp Hildebrand
(vice chairman)
Products	
Alternative investment
Asset management
ESG investment
Wealth management
Aladdin
Revenue	Increase US$24.22 billion (2025)
Operating income	Decrease US$7.045 billion (2025)
Net income	Decrease US$5.553 billion (2025)
AUM	Increase US$15.3 trillion (2026)
Total assets	Increase US$170.0 billion (2025)
Total equity	Increase US$55.89 billion (2025)
Number of employees	24,900 (2025)
Subsidiaries	
iShares
Global Infrastructure Partners
HPS Investment Partners
Website	blackrock.com
Footnotes

BlackRock, Inc. is an American multinational investment company. Founded in 1988, initially as an enterprise risk management and fixed income institutional asset manager, BlackRock is by far the world's largest asset manager,[1] with $15.3 trillion in assets under management as of 2026.[4][5] Headquartered in New York City, BlackRock has 70 offices in 30 countries and clients in 100 countries.[6]

BlackRock is the manager of the iShares group of exchange-traded funds, and along with Fidelity, Vanguard, and State Street, it is considered one of the Big Four index fund managers.[7][8] Its Aladdin software keeps track of investment portfolios for many major financial institutions and its BlackRock Solutions division provides financial risk management services. As of 2025, BlackRock was ranked 210th on the Fortune 500 list of the largest U.S. corporations by revenue.[9]"""
    summary_chunks = []
    async for chunk in call_google_api(conversation_contents):
        summary_chunks.append(chunk)
    return {"structured_summary": "".join(summary_chunks)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)