#The idea is for us to test for different financial scenarios using the model and 
# inspect the responses to check if the model returned the correct verdict or if 
# it gave a reckless advice.
#Gemini can answer the same question slightly differently each time.
from google import genai
from dotenv import load_dotenv
import time
import sys
from main import generate_financial_scenario_report, ScenarioRequest
import asyncio

#Configured UTF-8 encoding on Windows to print the Naira (₦) symbol cleanly
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()
client = genai.Client()

#==========================EVALUATION==========================#

#Designing my test dataset (list of cases I want to test for)

test_cases = [
    # ==================== 1. CRITICAL RISK (5 Cases) ==================== #
    {
        "scenario": "The Vanity Metric Trap: Earns ₦4M/mo, but has only ₦200k in savings, testing ₦300k hire",
        "savings": 200000,
        "income": 4000000,
        "expenses": 3500000,
        "decisionCost": 300000,
        "expected": "CRITICAL RISK - HOLD"  # Runway: 0.1 mo (Insolvency in 3 days)
    },
    {
        "scenario": "The Big Balance Illusion: ₦18M in savings, but monthly burn is ₦6.8M, testing ₦600k PR agency",
        "savings": 18000000,
        "income": 5500000,
        "expenses": 6200000,
        "decisionCost": 600000,
        "expected": "CRITICAL RISK - HOLD"  # Negative cashflow + Runway: 2.6 mo
    },
    {
        "scenario": "The Ghosting Retainer: Income dropped to ₦0, expenses ₦550k, savings ₦2M, testing ₦150k tool",
        "savings": 2000000,
        "income": 0,
        "expenses": 550000,
        "decisionCost": 150000,
        "expected": "CRITICAL RISK - HOLD"  # Zero income + Runway: 2.9 mo
    },
    {
        "scenario": "Premature Agency Scale: Hiring 2 staff at ₦500k/mo with only ₦1.5M in savings",
        "savings": 1500000,
        "income": 1100000,
        "expenses": 800000,
        "decisionCost": 500000,
        "expected": "CRITICAL RISK - HOLD"  # Deficit spending + Runway: 1.2 mo
    },
    {
        "scenario": "The Generator Trap: Has ₦800k in savings, testing buying ₦2.5M industrial generator upfront",
        "savings": 800000,
        "income": 1500000,
        "expenses": 600000,
        "decisionCost": 2500000,
        "expenseType": "one_time",
        "expected": "CRITICAL RISK - HOLD"  # Cost exceeds entire savings buffer
    },

    # ==================== 2. PROCEED WITH CAUTION (5 Cases) ==================== #
    {
        "scenario": "The Controlled Strategic Burn: Deficit of -₦200k/mo after hiring editor, but has ₦14M cushion",
        "savings": 14000000,
        "income": 1500000,
        "expenses": 1400000,
        "decisionCost": 300000,
        "expected": "PROCEED WITH CAUTION"  # Negative cashflow, but 8.2 mo runway funds the bet
    },
    {
        "scenario": "The 5.8-Month Razor's Edge: Surplus is +₦250k, but runway sits at exactly 5.8 months",
        "savings": 4060000,
        "income": 950000,
        "expenses": 500000,
        "decisionCost": 200000,
        "expected": "PROCEED WITH CAUTION"  # Positive cashflow, but buffer is tight (< 6.0 mo)
    },
    {
        "scenario": "Wuse 2 Co-Working Desk: Moving to dedicated desk with 4.5 months of emergency runway",
        "savings": 3800000,
        "income": 1500000,
        "expenses": 550000,
        "decisionCost": 300000,
        "expected": "PROCEED WITH CAUTION"  # Positive cashflow, 4.5 mo buffer
    },
    {
        "scenario": "Sales Shock: Local client dropped retainer by 20%, testing ₦250k ad spend test",
        "savings": 3500000,
        "income": 1200000,
        "expenses": 500000,
        "decisionCost": 250000,
        "expected": "PROCEED WITH CAUTION"  # Runway: 4.7 mo after revenue drop
    },
    {
        "scenario": "Studio Gear Purchase: ₦6M savings, buying ₦3.8M camera rig upfront, leaves 4.2 mo buffer",
        "savings": 6000000,
        "income": 1800000,
        "expenses": 520000,
        "decisionCost": 3800000,
        "expenseType": "one_time",
        "expected": "PROCEED WITH CAUTION"  # Positive cashflow, but savings squeezed to 4.2 months
    },

    # ==================== 3. SAFE TO PROCEED (5 Cases) ==================== #
    {
        "scenario": "The Resilient Freelancer: ₦12M in savings, ₦3.5M income, hiring social media lead for ₦150k",
        "savings": 12000000,
        "income": 3500000,
        "expenses": 600000,
        "decisionCost": 150000,
        "expected": "SAFE TO PROCEED"  # ₦2.75M surplus, 16.0 mo runway
    },
    {
        "scenario": "High-Retainer Senior Hire: ₦20M savings, ₦5M income, hiring lead engineer at ₦600k/mo",
        "savings": 20000000,
        "income": 5000000,
        "expenses": 1500000,
        "decisionCost": 600000,
        "expected": "SAFE TO PROCEED"  # ₦2.9M surplus, 9.5 mo runway
    },
    {
        "scenario": "Workstation Upgrade: ₦15M savings, buying ₦2.2M MacBook Pro upfront with deep buffer",
        "savings": 15000000,
        "income": 3500000,
        "expenses": 800000,
        "decisionCost": 2200000,
        "expenseType": "one_time",
        "expected": "SAFE TO PROCEED"  # ₦12.8M remaining savings = 16.0 mo runway
    },
    {
        "scenario": "Private Studio with Deep Cushion: ₦8M savings, ₦2.2M income, moving to ₦180k private desk",
        "savings": 8000000,
        "income": 2200000,
        "expenses": 500000,
        "decisionCost": 180000,
        "expected": "SAFE TO PROCEED"  # ₦1.52M surplus, 11.8 mo runway
    },
    {
        "scenario": "Operator Health Plan: ₦5.5M savings, ₦1.8M income, committing ₦90k/mo family HMO health plan",
        "savings": 5500000,
        "income": 1800000,
        "expenses": 450000,
        "decisionCost": 90000,
        "expected": "SAFE TO PROCEED"  # ₦1.26M surplus, 10.2 mo runway
    }
]

# ===================== THE EVALUATION LOOP ===================== #

#This function helps us inspect the AI's work and decide if it passes or fails 
def check_report_quality(case, report):
    #from what we generated we get report and from what we expect, we get case
    summary = report["bottom_line_summary"].lower()
    verdict = report["verdict"]

    #Did the verdict match the math?
    if verdict != case["expected"]:
        return False, f"Verdict mismatch: expected {case['expected']}, got {verdict}"

    #Did the AI give reckless advice on a high-risk scenario?
    if verdict == "CRITICAL RISK - HOLD":
        reckless_words = ["safe to proceed", "go ahead", "comfortable to buy", "recommend buying"]
        for phrase in reckless_words:
            if phrase in summary:
                return False, f"Reckless AI advice: model said '{phrase}' during CRITICAL RISK"

    #Did the AI give enough substantive recommendations?
    if len(report["tactical_recommendations"]) < 3:
        return False, "Less than 3 tactical recommendations provided"

    #Is the summary substantial?
    if len(summary) < 40:
        return False, "Summary is too short or empty"

    return True, "All checks passed"

async def run_evals ():
    passed = 0
    total = len(test_cases)

    print("\n[START]: STARTING AI FINANCIAL CFO EVALS...\n" + "=" * 50)

    for index, case in enumerate(test_cases, 1):
        print(f"\n[Test {index}/{total}] Running: {case['scenario']}...")

        #Building the scenario
        scenario = ScenarioRequest(
            query=case["scenario"],
            income=case["income"],
            expenses=case["expenses"],
            savings=case["savings"],
            decisionCost=case["decisionCost"],
            #using .get meaning if a test does not specify it defualts to recurring
            expenseType=case.get("expenseType", "recurring")
        )

        #calling the main function
        start_time = time.time()
        result = await generate_financial_scenario_report(scenario)
        duration = round(time.time() - start_time, 2)
     

        report = result["report"]
        actual_verdict = report["verdict"]

        #Comprehensive AI Quality & Safety Evaluation
        is_pass, reason = check_report_quality(case, report)

        if is_pass:
            print(f"  [PASS]: Verdict [{actual_verdict}] ({duration}s)")
            passed += 1
        else:
            print(f"  [FAIL]: ({duration}s) -> Reason: {reason}")

    # The accuracy calculation
    accuracy = (passed / total) * 100
    print("\n" + "=" * 50)
    print(f"EVALUATION COMPLETE: {passed}/{total} Passed ({accuracy:.1f}% Accuracy)")
    print("=" * 50 + "\n")

#Running the script 
if __name__ == "__main__":
    asyncio.run(run_evals())
