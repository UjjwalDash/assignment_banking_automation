#IMPORTS
from app.src.core.chain.recommendation_chain import RecommendationChain
from app.src.core.states.states import PlanExecute
from langgraph.graph import MessagesState

recommendation_chain_obj = RecommendationChain()
recommendation_chain_obj.load_configs()
recommendation_chain_obj.setup_recommendation()


# Difining Intent Elaborator Agent

async def recommendation_agent(state: PlanExecute):

    # Pass the input and retrieval result to the elaborator chain
    recommendation = await recommendation_chain_obj.get_recommendation_chain().ainvoke({
        "messages": [("user", state["input"])]
    })
    return {
        "Recommendation": recommendation.steps,
    }