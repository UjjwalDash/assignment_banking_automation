from pprint import pprint
from langchain_core.messages import HumanMessage

class DisputeInference:
    def __init__(self, graph):
        """
        Initializes the DisputeInference class with a recommendation graph.
        :param graph: The recommendation graph used for inference.
        """
        self.graph = graph

    async def inference(self, dispute):
        """
        Runs inference on the given dispute using the recommendation graph.
        
        :param dispute: The dispute description (text).
        :return: The recommendation result from the graph.
        """
        inputs = {"input": dispute}
        value = {}  # Ensure 'value' is defined before iteration
        
        async for event in self.graph.astream(inputs):
            for key, value in event.items():
                if key != "__end__":
                    print(f"Processing {key}: {value}")  # Debugging info

        # Extract recommendation safely to prevent KeyError
        return value.get("Recommendation", "No recommendation found")

# Example usage
# if __name__ == "__main__":
#     inference_engine = DisputeInference(recommendation_graph)
#     dispute = "Some dispute description here"
#     recommendation = await inference_engine.inference(dispute)
#     print("Recommendation:", recommendation)
