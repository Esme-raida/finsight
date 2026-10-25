from typing import Optional, Literal
from sqlmodel import SQLModel, Field
from datetime import datetime, timezone

#SCHEMAS(PYDANTIC BLUEPRINTS)

# ==================== DATABASE TABLE ==================== #

#Defining the table schema (just like a Pydantic model!)
class Scenario(SQLModel, table=True):
    #this defines the columns and primary key here means the keys are unique
    id: int | None = Field(default=None, primary_key=True)
    description: str
    savings: float
    monthly_burn: float
    runway_months: float
    verdict: str
    summary: Optional[str] = None #can be string or none 
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# ==================== API SCHEMAS (REQUEST / RESPONSE) ==================== #


#RESPONSE(output)#
class ExtractScenario(SQLModel):
    income: Optional[float] = None
    expenses: Optional[float] = None
    savings: Optional[float] = None
    decisionCost: Optional[float] = None
    decisionTitle: Optional[str] = None
    expenseType: Optional[Literal["recurring", "one_time"]] = "recurring"

class ExtractRequest(SQLModel):
    text: str

# Structured output mold for the Fractional CFO briefing
class CFOReportResponse(SQLModel):
    bottom_line_summary: str
    worst_case_analysis: str
    tactical_recommendations: list[str]



#REQUEST(input)#
class ScenarioRequest(SQLModel):
    query: str
    income: float = Field(..., ge=0, description="Monthly income in Naira")
    expenses: float = Field(..., ge=0, description="Monthly expenses in Naira")
    savings: float = Field(..., ge=0, description="Current cash savings in Naira")
    decisionCost: float = Field(..., ge=0, description="Cost of the decision in Naira")
    expenseType: Literal["recurring", "one_time"] = "recurring"


