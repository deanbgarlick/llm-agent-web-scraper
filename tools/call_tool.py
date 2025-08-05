"""
Tool execution functionality for handling OpenAI tool calls.
"""

import json
from typing import Dict, Any, Callable
from openai.types.chat import ChatCompletionMessageToolCall

def call_tool(tools_map: Dict[str, Callable[..., Any]], tool_call: ChatCompletionMessageToolCall) -> Dict[str, str]:
    """
    Execute a tool call using the provided tools map.
    
    Args:
        tools_map (Dict[str, Callable[..., Any]]): Dictionary mapping tool names to their implementations
        tool_call (ChatCompletionMessageToolCall): The tool call object from OpenAI
        
    Returns:
        Dict[str, str]: A message containing the tool call results in OpenAI's expected format
    """
    args = json.loads(tool_call.function.arguments) if isinstance(tool_call.function.arguments, str) else tool_call.function.arguments
    result = tools_map[tool_call.function.name](**args)
    tool_message = {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "name": tool_call.function.name,
        "content": str(result)
    }
    return tool_message 