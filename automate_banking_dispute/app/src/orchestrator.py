import asyncio
from pprint import pprint  # Pretty print for better readability of outputs
from langchain_core.messages import HumanMessage  # Importing message structure for handling interactions

# Importing necessary modules from the application's core functionalities
from app.src.core.priority_handler import TransactionPriority  # Handles transaction priority
from app.src.core.graph.graph import RecommendationGraph  # Handles recommendation graph
from app.src.core.inference import DisputeInference  # Performs inference on disputes
from app.src.core.risk_classifier import RiskClassifier  # Classifies the risk associated with disputes

class Orchestrator:
    def __init__(self):
        # Initialize the recommendation graph used for inference
        self.recommendation_graph = RecommendationGraph().get_graph()
        # Initialize the inference engine using the recommendation graph
        self.inference_engine = DisputeInference(self.recommendation_graph)

    async def process_dispute(self, user_id, dispute):
        # Fetch the priority of the transaction for the given user ID
        priority = TransactionPriority().get_priority(user_id)
        print("processing")
        
        # Perform inference to generate recommendations based on the dispute
        recommendation = await self.inference_engine.inference(dispute)
        
        # Format the recommendation if it is a list (multiple suggestions)
        if isinstance(recommendation, list):
            formatted_recommendation = "\n".join(f"{i+1}. {rec}" for i, rec in enumerate(recommendation))
        else:
            formatted_recommendation = recommendation
        
        # Determine the risk flag for the generated recommendation
        risk_flag = RiskClassifier().get_risk(formatted_recommendation)
        
        # Return the results including priority, risk flag, and recommendation
        return {
            "priority": priority,
            "risk_flag": risk_flag,
            "recommendation": formatted_recommendation
        }

# Example usage (commented out to prevent execution during imports)
# if __name__ == "__main__":
#     async def main():
#         orchestrator = Orchestrator()
#         dispute = "Some dispute description here"
#         user_id = 3  # Ensure this is an integer
#         priority, recommendation = await orchestrator.process_dispute(user_id, dispute)
#         print(priority, recommendation)
    
#     asyncio.run(main())  # Run async function properly
