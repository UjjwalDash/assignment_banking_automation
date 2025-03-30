import yaml
from app.models.models import recommendation_llm
from app.src.core.states.states import Recommendation
from langchain_core.prompts import ChatPromptTemplate

class RecommendationChain:
    def __init__(self):
        self.config_path = 'app/config/agents/agents.yaml'
        self.agent_config = None
        self.intent_prompt = ""
        self.intent_elaborator = None

    def load_configs(self):
        """Load the agent configuration from the specified YAML file."""
        with open(self.config_path, 'r') as file:
            self.agent_config = yaml.safe_load(file)

    def setup_recommendation(self):
        """Set up the intent elaborator prompt using the loaded configuration."""
        if not self.agent_config:
            raise ValueError("Agent configuration is not loaded.")

        recommendation_role = self.agent_config['recommendation_agent']['role']
        recommendation_goal = self.agent_config['recommendation_agent']['goal']
        recommendation_backstory = self.agent_config['recommendation_agent']['backstory']

        self.recommendation_prompt = (
            f"Your Role: {recommendation_role}\n"
            f"Your main goal: {recommendation_goal}\n"
            f"Backstory: {recommendation_backstory}"
        )

        recommendation_system_prompt = ChatPromptTemplate.from_messages([
            ("system", self.recommendation_prompt)
        ])
        # print(recommendation_system_prompt)
        self.recommendation = recommendation_system_prompt | recommendation_llm.with_structured_output(Recommendation)

    def get_recommendation_chain(self):
        """Return the configured intent elaborator."""
        if self.recommendation is None:
            raise ValueError("Intent elaborator is not set up.")
        return self.recommendation
