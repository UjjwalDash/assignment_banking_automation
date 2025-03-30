from langchain_groq import ChatGroq
import yaml

with open('app/config/models/models_config.yaml', 'r') as file:
    config = yaml.safe_load(file)

def load_grok_models(model_name, api_key, temperature):
    return ChatGroq(model=model_name, api_key = api_key, temperature = temperature)

model_name = config['recommendation']['model_name']
api_key = config['recommendation']['api_key']
temperature = config['recommendation']['temperature']

recommendation_llm = load_grok_models(model_name, api_key, temperature)