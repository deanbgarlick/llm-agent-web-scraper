from openai import OpenAI
from dotenv import load_dotenv
from utils.prompt_loader import load_prompt
from utils.chat_utils import set_client_and_model
from utils.tool_loader import load_tool_schemas
from tools import scrape, search, update_data
from agent.handlers import setup_event_handlers as setup_agent_event_handlers
from agent.agent import start_agent
from data_point_manager import get_data_point_manager

load_dotenv()


def _execute_scraping_agent(entity_name: str, tool_names: list, system_prompt_key: str, 
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
    data_keys_to_search = get_data_point_manager().get_missing_data_points()
    
    if len(data_keys_to_search) > 0:
        # Load prompts from files
        system_prompt = load_prompt(system_prompt_key)
        
        # Base replacements
        user_prompt_replacements = {
            "entity_name": entity_name,
            "links_scraped": str(links_scraped),
            "data_keys_to_search": str(data_keys_to_search)
        }
        
        # Add any additional replacements
        if dynamic_prompt_inserts:
            user_prompt_replacements.update(dynamic_prompt_inserts)
            
        user_prompt = load_prompt(user_prompt_key, user_prompt_replacements)
        
        response = start_agent(user_prompt, system_prompt, tool_schemas, tools_map, plan=False)
        return response
    
    return "No data points to search for"


def website_scrape(entity_name: str, website: str):
    """
    Scrape information about an entity from a specific website using scraping tools.
    
    Args:
        entity_name (str): Name of the entity to search for
        website (str): The website URL to scrape
    
    Returns:
        str: Response from the agent with found information
    """
    return _execute_scraping_agent(
        entity_name=entity_name,
        tool_names=["scrape", "update_data"],
        system_prompt_key='website_scrape_system',
        user_prompt_key='website_scrape_user',
        dynamic_prompt_inserts={"website": website}
    )


def internet_search_scrape(entity_name: str):
    """
    Search the internet and scrape relevant URLs to find information about an entity.
    
    Args:
        entity_name (str): Name of the entity to search for
    
    Returns:
        str: Response from the agent with found information
    """
    return _execute_scraping_agent(
        entity_name=entity_name,
        tool_names=["search", "scrape", "update_data"],
        system_prompt_key='internet_search_scrape_system',
        user_prompt_key='internet_search_scrape_user'
    )

# Example usage (commented out)
if __name__ == "__main__":
    entity_name = "Discord"
    website = "https://discord.com/"

    client = OpenAI()
    GPT_MODEL = "gpt-4-turbo-2024-04-09"

    # Initialize chat utilities with client and model
    set_client_and_model(client, GPT_MODEL)
    setup_agent_event_handlers()

    # Initialize global variables
    links_scraped = []

    data_points = [
        {"name": "num_employees", "value": None, "reference": None},
        {"name": "office_locations", "value": None, "reference": None},
        {"name": "main_product", "value": None, "reference": None},
    ]

    # Initialize the data manager with our data points
    get_data_point_manager(initial_data_points=data_points)

    response1 = website_scrape(entity_name, website)
    # response2 = internet_search_scrape(entity_name)

    print("------")
    print(f"Data points found: {get_data_point_manager().get_current_state()}")