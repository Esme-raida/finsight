#The idea is for us to test for different financial scenarios using the model and 
# inspect the responses to check if the model returned the correct verdict or if 
# it gave a reckless advice.
#Gemini can answer the same question slightly differently each time.
from google import genai
from dotenv import load_dotenv
import time

load_dotenv()
client = genai.Client()

#=====================EVALUATION=======================#
#Designing my test dataset(list of cases I want to test for)

test_cases = [
    # CRITICAL RISK 
    {
        "scenario": "Extreme Danger: Buying luxury car with only ₦150k in savings",
        "savings": 150000,
        "income": 400000,
        "expenses": 380000,
        "decisionCost": 2500000,
        "cashLeft": 400000 - (380000 + 2500000),
        "runwayMonths": 0.1,
        "expected": "CRITICAL RISK - HOLD"
    },
    {
        "scenario": "The Overhead Trap: Lekki rent + diesel eating 85% of income, testing ₦400k workspace",
        "savings": 1800000,
        "income": 1200000,
        "expenses": 1020000,
        "decisionCost": 400000,
        "cashLeft": 1200000 - (1020000 + 400000), # -₦220k monthly deficit!
        "runwayMonths": 1.2,
        "expected": "CRITICAL RISK - HOLD"
    },
    {
        "scenario": "The Ghosting Client: Client delays invoice, income drops to ₦0, testing ₦350k hire",
        "savings": 2000000,
        "income": 0,
        "expenses": 600000,
        "decisionCost": 350000,
        "cashLeft": 0 - (600000 + 350000), # -₦950k bleed/month
        "runwayMonths": 2.1,
        "expected": "CRITICAL RISK - HOLD"
    },
    {
        "scenario": "Premature Agency Scale: Hiring 2 full-time staff with only ₦1.5M in savings",
        "savings": 1500000,
        "income": 1000000,
        "expenses": 650000,
        "decisionCost": 600000,
        "cashLeft": 1000000 - (650000 + 600000), # -₦250k deficit
        "runwayMonths": 1.2,
        "expected": "CRITICAL RISK - HOLD"
    },

    # SAFE TO PROCEED
    {
        "scenario": "The Safe Expansion: ₦12M in savings, ₦3.5M income, hiring social media lead for ₦150k",
        "savings": 12000000,
        "income": 3500000,
        "expenses": 600000,
        "decisionCost": 150000,
        "cashLeft": 3500000 - (600000 + 150000), # ₦2.75M monthly surplus
        "runwayMonths": 16.0,
        "expected": "SAFE TO PROCEED"
    },

    # PROCEED WITH CAUTION
    {
        "scenario": "Productivity Workstation: ₦8M in savings, ₦2.5M income, buying M3 MacBook for ₦1.2M",
        "savings": 8000000,
        "income": 2500000,
        "expenses": 800000,
        "decisionCost": 1200000,
        "cashLeft": 2500000 - (800000 + 1200000), # ₦500k surplus left
        "runwayMonths": 7.0,
        "expected": "PROCEED WITH CAUTION"
    },
    {
        "scenario": "The Foreign Exchange Windfall: Landed $2,000/mo (₦3M) remote contract, buying ₦1.8M solar inverter",
        "savings": 9000000,
        "income": 3000000,
        "expenses": 700000,
        "decisionCost": 1800000,
        "cashLeft": 3000000 - (700000 + 1800000), # ₦500k surplus left in month 1
        "runwayMonths": 8.0,
        "expected": "PROCEED WITH CAUTION"
    },
    {
        "scenario": "The Co-Working Upgrade: Moving to Wuse 2 desk with 4.5 months of emergency runway",
        "savings": 3800000,
        "income": 1500000,
        "expenses": 550000,
        "decisionCost": 300000,
        "cashLeft": 1500000 - (550000 + 300000), # ₦650k surplus
        "runwayMonths": 4.5,
        "expected": "PROCEED WITH CAUTION"
    },
    {
        "scenario": "Sales Shock: Local client dropped retainer by 20%, testing ₦250k ad spend",
        "savings": 3500000,
        "income": 1200000,
        "expenses": 500000,
        "decisionCost": 250000,
        "cashLeft": 1200000 - (500000 + 250000), # ₦450k surplus
        "runwayMonths": 4.6,
        "expected": "PROCEED WITH CAUTION"
    },
    {
        "scenario": "Equipment Lease: Upgrading camera rig @ ₦350k/mo with ₦3M in savings",
        "savings": 3000000,
        "income": 1400000,
        "expenses": 600000,
        "decisionCost": 350000,
        "cashLeft": 1400000 - (600000 + 350000), # ₦450k surplus
        "runwayMonths": 3.8,
        "expected": "PROCEED WITH CAUTION"
    }
]
# ===================== THE EVALUATION LOOP ===================== #
passed = 0
total = len(test_cases)

print("\n[START]: STARTING AI FINANCIAL CFO EVALS...\n" + "=" * 50)

for index, case in enumerate(test_cases, 1):
    print(f"\n[Test {index}/{total}] Running: {case['scenario']}...")

    prompt = f"""
    You are an elite Fractional CFO in Nigeria.
    
    A client presents this scenario:
    - Savings: ₦{case['savings']:,.0f}
    - Monthly Income: ₦{case['income']:,.0f}
    - Monthly Expenses: ₦{case['expenses']:,.0f}
    - Proposed Decision Cost: ₦{case['decisionCost']:,.0f}/month
    - Emergency Runway: {case['runwayMonths']} months

    Choose ONE decision:
    1. SAFE TO PROCEED
    2. PROCEED WITH CAUTION
    3. CRITICAL RISK - HOLD

    Provide your decision and a 1-sentence explanation why.
    """

    start_time = time.time()

    # Call the model
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config={"temperature": 0}
    )
    duration = round(time.time() - start_time, 2)
    model_result = response.text

    # The simple check: did the model include the expected verdict?
    if case['expected'] in model_result:
        print(f"[PASS]: Found [{case['expected']}] ({duration}s)")
        passed += 1
    else:
        print(f"[FAIL]: Expected [{case['expected']}] ({duration}s)")
        print(f"   AI Output: {model_result.strip()}")

# The accuracy calculation
accuracy = (passed / total) * 100
print("\n" + "=" * 50)
print(f"EVALUATION COMPLETE: {passed}/{total} Passed ({accuracy:.1f}% Accuracy)")
print("=" * 50 + "\n")