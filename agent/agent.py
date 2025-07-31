"""
AI Agent module for handling conversations and tool interactions.

This module contains the core agent functionality for managing conversations
with AI models, handling tool calls, and coordinating between different
components of the system.
"""

from typing import Dict, List, Any, Callable
from utils.pretty_print import pretty_print_conversation
from utils.chat_utils import chat_completion_request
from agent.types import AgentResponseEventData, ToolCallResponseEventData, AgentFinishedEventData, ToolCallErrorEventData, AgentCallErrorEventData
from tools.executor import call_tool
from agent.publishers import publish_agent_response, publish_tool_call_response, publish_tool_call_error, publish_agent_call_error, publish_agent_finished


def start_agent(prompt: str, system_prompt: str, tools_schema: List[Dict], tools_map: Dict, plan: bool = False) -> str:
    """
    Run a conversation with the AI agent using the provided prompts and tools.
    
    Args:
        prompt (str): The user's prompt to the agent
        system_prompt (str): The system instructions for the agent
        tools_schema (List[Dict]): OpenAI function calling schema for available tools
        tools_map (Dict): Dictionary mapping tool names to actual Python functions
        plan (bool, optional): Whether to ask the agent to plan first. Defaults to False.
    
    Returns:
        str: The final response from the agent
    """
    messages = create_initial_messages(system_prompt, prompt, tools_schema, plan)

    # Print initial messages
    for message in messages:
        pretty_print_conversation(message)

    send_messages_to_agent(messages, tools_schema, tools_map)


def create_initial_messages(system_prompt: str, prompt: str, tools_schema: List[Dict], tools_map: Dict, plan: bool = False) -> List[Dict]:
    messages = []
    if plan:
        planning_prompt = f"{system_prompt} {prompt} Let's think step by step, make a plan first"
        messages.append({"role": "user", "content": planning_prompt})
        
        # Get initial plan
        chat_response = chat_completion_request(messages, tool_choice="none", tools=tools_schema)
        if isinstance(chat_response, Exception):
            publish_agent_call_error(AgentCallErrorEventData(
                messages=messages,
                tools_map=tools_map,
                tools_schema=tools_schema,
                error=chat_response
            ))
            return f"Failed to create plan: {str(chat_response)}"
            
        plan_content = chat_response.choices[0].message.content
        messages = [
            {"role": "user", "content": f"{system_prompt} {prompt}"},
            {"role": "assistant", "content": plan_content}
        ]
    else:
        messages.append({"role": "user", "content": f"{system_prompt} {prompt}"})
    return messages


def send_messages_to_agent(
    messages: List[Dict[str, str]], 
    tools_schema: List[Dict], 
    tools_map: Dict[str, Callable[..., Any]]
) -> None:

    chat_response = chat_completion_request(messages, tool_choice=None, tools=tools_schema)
    
    if isinstance(chat_response, Exception):
        print("Failed to get a valid response:", chat_response)
        return
        
    # Process the response
    current_choice = chat_response.choices[0]
    assistant_message = {
        "role": "assistant",
        "content": current_choice.message.content,
        "tool_calls": current_choice.message.tool_calls
    }
    messages.append(assistant_message)
    publish_agent_response(AgentResponseEventData(
        chat_response=chat_response,
        messages=messages,
        tools_map=tools_map,
        tools_schema=tools_schema
    ))


def process_agent_response(event_data: AgentResponseEventData):
    # Handle tool calls if any

    current_choice = event_data.chat_response.choices[0]
    # assistant_message = {
    #     "role": "assistant",
    #     "content": current_choice.message.content,
    #     "tool_calls": current_choice.message.tool_calls
    # }
    # event_data.messages.append(assistant_message)

    # Check if conversation should end
    if current_choice.finish_reason == "stop":
        publish_agent_finished(AgentFinishedEventData(
            messages=event_data.messages
        ))
        return
    
    elif current_choice.finish_reason == "tool_calls":
        _call_chosen_tools(event_data)
    else:
        raise ValueError(f"Invalid finish reason: {current_choice.finish_reason}")
        

def _call_chosen_tools(event_data: AgentResponseEventData):

    current_choice = event_data.chat_response.choices[0]

    tool_calls = current_choice.message.tool_calls
    for tool_call in tool_calls:
        function = tool_call.function
        try:

            tool_message = call_tool(event_data.tools_map, tool_call)
            event_data.messages.append(tool_message)
            publish_tool_call_response(ToolCallResponseEventData(
                messages=event_data.messages,
                tools_map=event_data.tools_map,
                tools_schema=event_data.tools_schema
            ))
            
        except Exception as e:
            print(f"Tool call failed: {str(e)}")
            error_message = {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": function.name,
                "content": f"Error: {str(e)}"
            }
            event_data.messages.append(error_message)
            publish_tool_call_error(ToolCallErrorEventData(
                messages=event_data.messages,
                tools_map=event_data.tools_map,
                tools_schema=event_data.tools_schema,
                error=e
            ))
        finally:
            return