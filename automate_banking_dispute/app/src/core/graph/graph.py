from langgraph.graph import StateGraph, START, END
from app.src.core.agent import recommendation_agent
from app.src.core.states.states import PlanExecute

class RecommendationGraph:
    """
    Defines a recommendation graph for executing inference tasks
    based on the PlanExecute state.
    """
    
    def __init__(self):
        """
        Initializes the graph builder and compiles the state graph.
        """
        self.builder = StateGraph(PlanExecute)
        self._build_graph()  # Call method to define the graph structure
        self.graph = self.builder.compile()  # Compile the graph for execution

    def _build_graph(self):
        """
        Defines nodes and edges for the recommendation graph.
        """
        # Add a recommendation agent node
        self.builder.add_node("recommendation_agent", recommendation_agent.recommendation_agent)
        
        # Define the graph flow: START → recommendation_agent → END
        self.builder.add_edge(START, "recommendation_agent")
        self.builder.add_edge("recommendation_agent", END)

    def get_graph(self):
        """
        Returns the compiled recommendation graph.
        :return: The compiled state graph.
        """
        return self.graph

# Instantiate and retrieve the compiled graph
# recommendation_graph = RecommendationGraph().get_graph()
