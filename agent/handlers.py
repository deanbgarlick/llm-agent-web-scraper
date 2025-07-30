from agent.types import ToolCallResponseEventData, ToolCallErrorEventData, AgentFinishedEventData, AgentResponseEventData, AgentCallErrorEventData
from agent.agent import send_messages_to_agent, memory_optimise, process_agent_response
from event import subscribe
from utils.pretty_print import pretty_print_conversation

def handle_tool_call_response(event_data: ToolCallResponseEventData):
    pretty_print_conversation(event_data.messages[-1])
    messages = memory_optimise(event_data.messages)
    send_messages_to_agent(messages, event_data.tools_schema, event_data.tools_map)

def handle_agent_response(event_data: AgentResponseEventData):
    pretty_print_conversation(event_data.messages[-1])
    process_agent_response(event_data)

def handle_agent_finished(event_data: AgentFinishedEventData):
    pretty_print_conversation(event_data.messages[-1])
    pass

def handle_tool_call_error(event_data: ToolCallErrorEventData):
    pretty_print_conversation(event_data.messages[-1])
    raise event_data.error

def handle_agent_call_error(event_data: AgentCallErrorEventData):
    pretty_print_conversation(event_data.messages[-1])
    raise event_data.error

def setup_event_handlers():
    subscribe("agent_response", handle_agent_response)
    subscribe("tool_call_response", handle_tool_call_response)
    subscribe("agent_finished", handle_agent_finished)
    subscribe("tool_call_error_response", handle_tool_call_error)
    subscribe("agent_call_error", handle_agent_call_error)
