from termcolor import colored

def pretty_print_conversation(message):
    """
    Pretty print a conversation message with color coding based on role.
    
    Args:
        message (dict): Message dictionary containing 'role' and 'content' keys,
                       optionally 'tool_calls' for assistant messages
    """
    role_to_color = {
        "system": "red",
        "user": "green",
        "assistant": "blue",
        "tool": "magenta",
    }
    
    role = message.get("role", "unknown")
    color = role_to_color.get(role, "white")
    
    if role == "system":
        print(colored(f"system: {message['content']}\n", color))
        
    elif role == "user":
        print(colored(f"user: {message['content']}\n", color))
        
    elif role == "assistant":
        if message.get("tool_calls"):
            # For tool calls, print each one separately
            print(colored("assistant: Using tools:", color))
            for tool_call in message["tool_calls"]:
                function = tool_call.function
                # Access function attributes with dot notation, not dictionary notation
                print(colored(f"  - {function.name}: {function.arguments}\n", color))
        else:
            # For regular assistant messages
            print(colored(f"assistant: {message.get('content', '')}\n", color))
            
    elif role == "tool":
        # For tool responses - handle both dictionary and string name formats
        tool_name = message.get("name", "unknown_tool")
        if isinstance(tool_name, dict):
            tool_name = tool_name.get("name", "unknown_tool")
        # print(colored(f"tool ({tool_name}): {message.get('content', '')}\n", color))
    
    else:
        # Fallback for unknown message types
        print(colored(f"unknown ({role}): {message.get('content', '')}\n", "white")) 