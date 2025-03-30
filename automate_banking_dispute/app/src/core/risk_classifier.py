class RiskClassifier:
    def __init__(self):
        # Define risk categories in descending order of severity
        self.risk_type = ["high", "medium", "low"]

    def get_risk(self, agent_response):
        """
        Determines the risk level based on the agent's response.

        :param agent_response: str - The response from the agent to be analyzed
        :return: str - Risk level ('high', 'medium', 'low') or 'unknown' if not found
        """
        # Convert response to lowercase for case-insensitive matching
        agent_response = agent_response.lower()

        # Check if any risk type is present in the response
        for risk in self.risk_type:
            if risk in agent_response:
                return risk

        return "unknown"  # Return 'unknown' instead of None for better handling
