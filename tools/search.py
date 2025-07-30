import json
from firecrawl import FirecrawlApp
from utils.prompt_loader import load_prompt
import utils.chat_utils as chat_utils


def search(query, entity_name: str):
    """
    Search for information about an entity using FirecrawlApp and process results with GPT.
    
    Args:
        query (str): The search query to execute
        entity_name (str): Name of the entity to search information about
    
    Returns:
        dict: JSON response containing found information and related URLs to scrape
    """
    try:
        app = FirecrawlApp()
        
        # Configure search parameters
        
        # Execute search
        search_result = app.search(query)
        search_result_str = str(search_result)
        
        # Import data_points from the main module
        from app import data_points
        
        # Get list of data points we still need to find
        data_keys_to_search = [obj["name"] for obj in data_points if obj["value"] is None]
        
        # Load and format the prompt template
        replacements = {
            "entity_name": entity_name,
            "search_results": search_result_str,
            "data_points": ', '.join(data_keys_to_search)
        }
        prompt = load_prompt('parse_search_result', replacements)
        
        # Get structured response from GPT
        response = chat_utils.client.chat.completions.create(
            model=chat_utils.GPT_MODEL,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        try:
            result = json.loads(response.choices[0].message.content)
            return result
        except json.JSONDecodeError:
            print("Error: Failed to parse GPT response as JSON")
            return {"related urls to scrape further": [], "info found": []}
            
    except Exception as e:
        print(f"Search failed: {str(e)}")
        return {"related urls to scrape further": [], "info found": []} 