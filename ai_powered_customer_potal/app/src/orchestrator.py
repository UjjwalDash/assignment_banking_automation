import asyncio
from pprint import pprint
from langchain_core.messages import HumanMessage
from app.src.core.loan_eligiblity_calculator import LoanEligibilityCalculator
from app.src.core.graph.graph import RecommendationGraph
from app.src.core.inference import DisputeInference

class Orchestrator:
    def __init__(self):
        # Initialize the recommendation graph used for inference
        self.recommendation_graph = RecommendationGraph().get_graph()
        # Initialize the inference engine using the recommendation graph
        self.inference_engine = DisputeInference(self.recommendation_graph)

    async def process_loan(self, data):
        loan_eligiblity_score = LoanEligibilityCalculator(**data).calculate_score()
        print("processing")
        # Perform inference to generate recommendations based on the data
        recommendation = await self.inference_engine.inference(data)
        
        if isinstance(recommendation, list):
            formatted_recommendation = "\n".join(f"{i+1}. {rec}" for i, rec in enumerate(recommendation))
        else:
            formatted_recommendation = recommendation
            
        return {
            "loan_eligiblity_score": loan_eligiblity_score,
            "recommendation": formatted_recommendation
        }

