from pathlib import Path
from typing import Dict, Optional

def load_prompt(template_name: str, replacements: Optional[Dict[str, str]] = None) -> str:
    """
    Load a prompt template and format it with the provided replacements.
    
    Args:
        template_name (str): Name of the template file (without .txt extension)
        replacements (Dict[str, str], optional): Dictionary of placeholder replacements where
            keys are the placeholder names and values are their replacements
    
    Returns:
        str: Formatted prompt
    
    Example:
        >>> replacements = {
        ...     "entity_name": "Discord",
        ...     "search_results": "Result text...",
        ...     "data_points": "employees, revenue"
        ... }
        >>> prompt = load_prompt("search", replacements)
    """
    prompts_dir = Path(__file__).parent.parent / 'prompts'
    template_path = prompts_dir / f"{template_name}.txt"
    
    try:
        with open(template_path, 'r') as f:
            template = f.read()
            
        if replacements:
            return template.format(**replacements)
        return template
            
    except FileNotFoundError:
        raise FileNotFoundError(f"Prompt template '{template_name}' not found")
    except KeyError as e:
        raise KeyError(f"Missing required placeholder in prompt template: {e}")
    except ValueError as e:
        raise ValueError(f"Error formatting prompt template: {e}") 