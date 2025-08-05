import json
from pathlib import Path
from typing import List, Dict, Union

def load_tool_schema(tool_name: str) -> Dict:
    """
    Load a single tool schema from a JSON file.
    
    Args:
        tool_name (str): Name of the tool (without .json extension)
    
    Returns:
        Dict: Tool schema dictionary
    """
    tools_dir = Path(__file__).parent.parent / 'tools'
    tool_path = tools_dir / f"{tool_name}_tool_schema.json"
    
    try:
        with open(tool_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Tool schema '{tool_name}' not found at {tool_path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in tool schema '{tool_name}': {e}")

def load_tool_schemas(tools: Union[List[str], str]) -> List[Dict]:
    """
    Load multiple tool schemas from JSON files or a predefined tool set.
    
    Args:
        tools (Union[List[str], str]): Either a list of tool names or a tool set name
    
    Returns:
        List[Dict]: List of tool schema dictionaries
    """
    if isinstance(tools, str):
        # Load predefined tool set
        tool_names = load_tool_set(tools)
    else:
        # Use provided list of tool names
        tool_names = tools
    
    schemas = []
    for tool_name in tool_names:
        schemas.append(load_tool_schema(tool_name))
    return schemas

def load_tool_set(set_name: str) -> List[str]:
    """
    Load a predefined tool set from configuration.
    
    Args:
        set_name (str): Name of the tool set
    
    Returns:
        List[str]: List of tool names in the set
    """
    config_dir = Path(__file__).parent.parent / 'config'
    config_path = config_dir / 'tool_sets.json'
    
    try:
        with open(config_path, 'r') as f:
            tool_sets = json.load(f)
            
        if set_name not in tool_sets:
            raise ValueError(f"Tool set '{set_name}' not found. Available sets: {list(tool_sets.keys())}")
            
        return tool_sets[set_name]
        
    except FileNotFoundError:
        raise FileNotFoundError(f"Tool sets configuration not found at {config_path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in tool sets configuration: {e}")

def get_available_tools() -> List[str]:
    """
    Get a list of all available tool names by scanning the tools directory.
    
    Returns:
        List[str]: List of available tool names (without _tool_schema.json suffix)
    """
    tools_dir = Path(__file__).parent.parent / 'tools'
    tool_files = tools_dir.glob("*_tool_schema.json")
    return [f.stem.replace("_tool_schema", "") for f in tool_files]

def get_available_tool_sets() -> List[str]:
    """
    Get a list of all available tool set names.
    
    Returns:
        List[str]: List of available tool set names
    """
    config_dir = Path(__file__).parent.parent / 'config'
    config_path = config_dir / 'tool_sets.json'
    
    try:
        with open(config_path, 'r') as f:
            tool_sets = json.load(f)
        return list(tool_sets.keys())
    except (FileNotFoundError, json.JSONDecodeError):
        return [] 