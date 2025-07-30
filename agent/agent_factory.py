from openai import OpenAI
from dotenv import load_dotenv
from utils.prompt_loader import load_prompt
from utils.chat_utils import set_client_and_model
from utils.tool_loader import load_tool_schemas
from tools import scrape, search, update_data
from agent.agent import start_agent
from agent.handlers import setup_event_handlers

load_dotenv()

client = OpenAI()
GPT_MODEL = "gpt-4-turbo-2024-04-09"

# Initialize chat utilities with client and model
set_client_and_model(client, GPT_MODEL)


# Initialize global variables
LINKS_SCRAPED = []

DATA_POINTS = [
    {"name": "catering_offering_for_employees", "value": None, "reference": None},
    {"name": "num_employees", "value": None, "reference": None},
    {"name": "office_locations", "value": None, "reference": None},
    # {"name": "main_product", "value": None, "reference": None},
]

def create_scraping_agent(entity_name: str, tool_names: list, system_prompt_key: str, 
                           user_prompt_key: str, dynamic_prompt_inserts: dict = None):
    """
    Common function to execute scraping agents with different configurations.
    
    Args:
        entity_name (str): Name of the entity to search for
        tool_names (list): List of tool names to load schemas for
        system_prompt_key (str): Key for the system prompt file
        user_prompt_key (str): Key for the user prompt file
        dynamic_prompt_inserts (dict): Additional replacements for user prompt
    
    Returns:
        str: Response from the agent with found information
    """
    setup_event_handlers()

    # Load tool schemas from JSON files
    tool_schemas = load_tool_schemas(tool_names)
    
    # Available tool functions
    available_tools = {
        "search": search,
        "scrape": scrape,
        "update_data": update_data
    }
    
    # Map only the requested tool names to actual functions
    tools_map = {name: available_tools[name] for name in tool_names}
    
    # Get data points we still need to find
    data_keys_to_search = [obj["name"] for obj in DATA_POINTS if obj["value"] is None]
    
    if len(data_keys_to_search) > 0:
        # Load prompts from files
        system_prompt = load_prompt(system_prompt_key)
        
        # Base replacements
        user_prompt_replacements = {
            "entity_name": entity_name,
            "links_scraped": str(LINKS_SCRAPED),
            "data_keys_to_search": str(data_keys_to_search)
        }
        
        # Add any additional replacements
        if dynamic_prompt_inserts:
            user_prompt_replacements.update(dynamic_prompt_inserts)
            
        user_prompt = load_prompt(user_prompt_key, user_prompt_replacements)
        
        response = start_agent(user_prompt, system_prompt, tool_schemas, tools_map, plan=False)
        return response
    
    return "No data points to search for"