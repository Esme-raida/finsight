#IMPORTING ALL PACKAGES & TOOLS
#Extrenal Imports
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import time
import os
import json
#Imports from other files
from sqlmodel import Session, select
from database import init_db, get_session
from models import Scenario, ExtractRequest, ScenarioRequest
from cfo_service import extract_financial_data, generate_financial_scenario_report
from calculator import calculate_metrics


#an instance of fastAPI
app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db() #This creates the database table when the server starts

#allowing the frontend (React / Vercel / Local) to communicate with the backend
app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], # Allows Vercel preview URLs, production domains, and localhost
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {
        "status": "online",
        "service": "FinSight Fractional CFO & Runway Decision Engine",
        "documentation": "/docs"
    }

#FOR GETTING FINANCIAL SCENARIO REPORT
@app.post("/api/report")
async def get_report( scenario: ScenarioRequest, session: Session = Depends(get_session)):

    #Doing the pure math
    metrics = calculate_metrics(
        income=scenario.income,
        expenses=scenario.expenses,
        savings=scenario.savings,
        decision_cost=scenario.decisionCost,
        expenseType=scenario.expenseType
    )

    #Asking our AI Chef in cfo_service.py for the briefing!
    report_data = await generate_financial_scenario_report(
        query=scenario.query, 
        metrics=metrics, 
        expense_type=scenario.expenseType
    )

    #Saving the scenario to the database
    db_scenario = Scenario( 
        description=scenario.query, 
        savings=metrics["savings"],
        monthly_burn=metrics["total_monthly_burn"],
        runway_months=metrics["runway_months"],
        verdict=metrics["verdict"]
    )
    session.add(db_scenario) #staging it - it works like git add .
    session.commit() #this actually commits the staged data and writes to the SQLite file on th disk
    session.refresh(db_scenario)  #this ensures the returned scenario has its auto-generated database id

    #returning react
    return {
        "status": "success",
        "metrics": metrics,
        "report": report_data
    }



#FOR RETRIEVING PAST SCENARIOS
@app.get("/api/scenarios")
def get_saved_scenarios(session: Session = Depends(get_session)):
    statement = select(Scenario) #this is like writing SELECT * FROM scenario;
    scenarios = session.exec(statement).all() #this executes the query and returns all rows as a list
    return scenarios #FASTAPI converts that list to JSON


#FOR EXTRACTING FINANCIAL DATA FROM USER INPUT
@app.post("/api/extract")
async def get_data (request: ExtractRequest):
    data = await extract_financial_data(request.text)
    #finally returning the output
    return {
        "status": "success",
        "data": data
    }