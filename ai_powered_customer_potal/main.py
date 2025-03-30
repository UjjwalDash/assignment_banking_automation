import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from app.src.orchestrator import Orchestrator  # Importing Orchestrator

app = FastAPI()
orchestrator = Orchestrator()  # Instantiate the orchestrator

# Define the expected request payload structure
class DisputeRequest(BaseModel):
    age: int
    employment_type: str
    residence_type: str
    monthly_income: int
    other_income: int
    total_emi: int
    savings: int
    bank_balance: int
    credit_score: int
    existing_loans: int
    past_defaults: bool
    credit_utilization: int
    loan_amount: int
    loan_type: str
    down_payment: int
    collateral: bool
    legal_issues: bool
    guarantor: bool

@app.post("/process_loan/")
async def process_dispute(request: DisputeRequest):
    print("Received dispute request")
    
    # Ensure process_dispute is an async function in Orchestrator
    result = await orchestrator.process_loan(request.dict())  
    return {"status": "success", "data": result}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, reload=True)
