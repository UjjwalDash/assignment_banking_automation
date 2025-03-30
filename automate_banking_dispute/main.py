import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from app.src.orchestrator import Orchestrator  # Importing Orchestrator

app = FastAPI()
orchestrator = Orchestrator()  # Instantiate the orchestrator

class DisputeRequest(BaseModel):
    user_id: int
    dispute: str

@app.post("/process_dispute/")
async def process_dispute(request: DisputeRequest):
    print("received")
    result = await orchestrator.process_dispute(request.user_id, request.dispute)
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, reload=True)

    # Example usage
# if __name__ == "__main__":
    # async def main():
    #     orchestrator = Orchestrator()
    #     dispute = "My credit card was charged $89.99 for a subscription I canceled last month. I have the email confirmation of cancellation dated May 15th"
    #     user_id = 3  # Ensure this is an integer
    #     answer = await orchestrator.process_dispute(user_id, dispute)
    #     print(answer)
    
    # asyncio.run(main())  # Run async function properly
