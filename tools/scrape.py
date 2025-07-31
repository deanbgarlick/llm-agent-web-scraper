from firecrawl import FirecrawlApp
from data_manager import get_data_manager


def scrape(url):
    """
    Scrape a single URL and return the markdown content.
    
    Args:
        url (str): The URL to scrape
    
    Returns:
        str: The markdown content of the scraped page, or error message
    """
    app = FirecrawlApp()
    
    # Scrape a single URL
    try:
        scraped_data = app.scrape_url(url)
        
        # Handle different response formats from FirecrawlApp
        if hasattr(scraped_data, 'markdown'):
            # If it's an object with markdown attribute
            markdown_content = scraped_data.markdown
        elif isinstance(scraped_data, dict) and 'markdown' in scraped_data:
            # If it's a dictionary with markdown key
            markdown_content = scraped_data['markdown']
        elif hasattr(scraped_data, 'content'):
            # If it has content attribute
            markdown_content = scraped_data.content
        else:
            # Fallback - convert to string
            markdown_content = str(scraped_data)
            
        # Add scraped link to manager
        get_data_manager().add_scraped_link(url)
        return markdown_content
        
    except Exception as e:
        error_msg = f"Unable to scrape the url {url}: {str(e)}"
        print(error_msg)
        return error_msg
