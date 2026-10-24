#============================= DETERMINISTIC MATH ENGINE =============================#

def calculate_metrics(income: float, expenses: float, savings: float, 
                    decision_cost: float, expenseType: str = "recurring") -> dict:
    #CapEx - Capital Expenditure (One-off Purchases)
    if expenseType == "one_time" :
        effective_savings = max(0.0, savings - decision_cost)
        total_monthly_burn = expenses
        cash_left = income - total_monthly_burn
        runway_months = round(effective_savings / total_monthly_burn, 1) if total_monthly_burn > 0 else 99.0
        
        # If cost exceeds savings, runway after purchase is 0
        if decision_cost > savings:
            runway_months = 0.0

    #OpEx - Operational Expenditure (Recurring Costs)
    else:
        effective_savings = savings
        total_monthly_burn = expenses + decision_cost
        cash_left = income - total_monthly_burn
        runway_months = round(effective_savings / total_monthly_burn, 1) if total_monthly_burn > 0 else 99.0
    

    #For determining the verdict
    if expenseType == "one_time" and decision_cost >= savings:
        verdict ="CRITICAL RISK - HOLD" 
    elif cash_left > 0 and runway_months >= 6.0:
        verdict = "SAFE TO PROCEED"
    elif (cash_left >= 0 and 3.0 <= runway_months < 6.0) or (cash_left < 0 and runway_months >= 6.0):
        verdict = "PROCEED WITH CAUTION"
    else:
        verdict = "CRITICAL RISK - HOLD"

    stressed_income = income * 0.8
    stressed_cash_left = stressed_income - total_monthly_burn

    return {
        "income": income,
        "expenses": expenses,
        "savings": savings,
        "decision_cost": decision_cost,
        "effective_savings": effective_savings,
        "total_monthly_burn": total_monthly_burn,
        "cash_left": cash_left,
        "runway_months": runway_months,
        "verdict": verdict,
        "stressed_cash_left": stressed_cash_left
    }
