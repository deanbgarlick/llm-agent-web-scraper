from event import publish
from agent.types import AgentResponseEventData, ToolCallResponseEventData, ToolCallErrorEventData, AgentCallErrorEventData, AgentFinishedEventData

def publish_agent_response(event_data: AgentResponseEventData):
    publish("agent_response", event_data)

def publish_tool_call_response(event_data: ToolCallResponseEventData):
    publish("tool_call_response", event_data)

def publish_agent_finished(event_data: AgentFinishedEventData):
    publish("agent_finished", event_data)

def publish_tool_call_error(event_data: ToolCallErrorEventData):
    publish("tool_call_error_response", event_data)

def publish_agent_call_error(event_data: AgentCallErrorEventData):
    publish("agent_call_error", event_data)
