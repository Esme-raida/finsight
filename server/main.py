#IMPORTING ALL PACKAGES
#from package import  tool
from fastapi import FastAPI
#importing pydantic from the base model
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import time
import os
import asyncio
import json
from dotenv import load_dotenv
from google import genai
from typing import Optional

#helps us look into .env to grab the API Key
load_dotenv()
#initializing the genai client
client = genai.Client()

#helper function for calling the gemini API
async def call_gemini_with_retry(prompt, config=None, retries=2):
    if config is None:
        config={"temperature": 0}
    for attempt in range(retries + 1):
        try:
            return await asyncio.to_thread (
                client.models.generate_content,
                model="gemini-3.5-flash-lite",
                contents=prompt,
                config=config
            )
        except Exception as e:
            if attempt == retries:
                print(f"[ERROR] Gemini call failed after {retries} retries: {e}")
                raise e

            wait_time = 2 ** attempt
            print(f"[WARN] Gemini call failed (attempt {attempt + 1}/{retries + 1}). Retrying in {wait_time}s")
            await asyncio.sleep(wait_time)


#an instance of fastAPI
app = FastAPI()
#Allowed frontend oigins
origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        #"https://finsight.vercel.app
]
#allowing the frontend(REACT) to communicate with the backend(FASTAPI)
app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins, #React app's address
    allow_credentials=True,
    allow_methods=["*"], #allows all HTTP methods like GET, POST, etc.
    allow_headers=["*"], #allows all headers
)

#SCHEMAS(PYDANTIC BLUEPRINTS)

#for output
#this is my pydantic schema contract that guarantees the data has the exact types and keys specified
class ExtractScenario(BaseModel):
    income: Optional[float] = None
    expenses: Optional[float] = None
    savings: Optional[float] = None
    decisionCost: Optional[float] = None
    decisionTitle: Optional[str] = None

class ExtractRequest(BaseModel):
    text: str


#for input 
#for generating the financial scenario report...this is to be extracted from the input passed by the user
class ScenarioRequest(BaseModel):
    query: str #expecting a string
    income: float #expecting a float
    expenses: float
    savings: float
    decisionCost: float
    cashLeft: float
    runwayMonths: float

#making or sending data to be processed    
@app.post("/api/report")

async def generate_financial_scenario_report(scenario: ScenarioRequest):

    prompt = f"""You are an elite Fractional CFO, with 20 years of experience who has guided High-Net Worth
    individuals and independent operators in Nigeria's ever-evolving and dynamic economy with their
    finances and financial decisions. You are known for exceptional and oustanding financial guidance 
    and insightful analysis. You are to provide tailored, pragmatic, candid and decisive financial guidance 
    with context to the question asked by the user. Your answers should be professional, precise, friendly
    and clear, no formal financial jargon.
    Communication Rule: 
    Explain things like a trusted, smart friend over coffee. 
    Assume the user has zero financial background.
    Avoid all corporate boardroom speak. Be warm, plain-spoken, and grounded in everyday Nigerian life.

    Here is the scenario data:

    - Question: {scenario.query}
    - Monthly Income: ₦{scenario.income:,.0f}
    - Baseline Expenses: ₦{scenario.expenses:,.0f}
    - Savings Buffer: ₦{scenario.savings:,.0f}
    - Proposed Decision Cost: ₦{scenario.decisionCost:,.0f}/month
    - Cash Left After Decision: ₦{scenario.cashLeft:,.0f}/month
    - Emergency Runway: {scenario.runwayMonths} months
    
    Generate a response with the following structure:
    ### 1. Can You Afford It?
    Give a clear decision: SAFE TO PROCEED, PROCEED WITH CAUTION, or CRITICAL RISK - HOLD.
    Provide a 1-2 sentence bottom-line summary explaining why.
    ### 2. The Worst-Case Check
    Analyze what happens if client payments lag by 30 to 60 days. Reference their actual runway and cash left numbers.
    ### 3. How To Play It Safe
    Give 3 concrete, bulleted recommendations the operator can execute right now to mitigate risk.
    Keep the total response under 300 words. Be direct, authoritative, and concise.

    """

    response= await call_gemini_with_retry(prompt)
    #finally returning the output
    return {
    "status": "success",
    "report": response.text
        }

@app.post("/api/extract")

async def extract_financial_data(request: ExtractRequest):
    prompt = f"""
    You are an expert world-class Financial Data Extraction Specialist. 
    Your job is to read the raw text provided by a user and extract financial 
    figures into structured data.

    EXTRACTION RULES:
    1. Extract numerical values for: income, expenses, savings, and decisionCost.
    2. Convert financial shorthand into full numbers:
       - "k" or "thousand" = multiply by 1,000 (e.g., "500k" -> 500000)
       - "m" or "million" = multiply by 1,000,000 (e.g., "2.5m" -> 2500000)
    3. Extract a short summary of the decision into "decisionTitle" (e.g., "Hire a designer").
    4. If any numerical value is not mentioned or impossible to determine, set its value to null.
    5. Do not invent or assume numbers that were not provided.
    USER INPUT TO ANALYZE:
    <user_query>
    {request.text}
    </user_query>
    """
 
    response= await call_gemini_with_retry(prompt, config={ 
                "temperature": 0,
                "response_mime_type":"application/json",
                "response_schema":ExtractScenario
                    }
            )
    #finally returning the output
    return {
    "status": "success",
    "data": json.loads(response.text)
}
