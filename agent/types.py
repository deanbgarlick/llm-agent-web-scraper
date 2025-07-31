from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class ResponseEventData:
    messages: List[Dict]
    tools_map: Dict
    tools_schema: List[Dict]
    chat_response: Optional[Dict] = None  # Optional since tool responses don't have this

@dataclass
class LlmErrorEventData:
    messages: List[Dict]
    tools_map: Dict
    tools_schema: List[Dict]
    error: Exception

@dataclass
class ToolCallResponseEventData(ResponseEventData):
    pass

@dataclass
class ToolCallErrorEventData(LlmErrorEventData):
    pass

@dataclass
class AgentResponseEventData(ResponseEventData):
    pass

@dataclass
class AgentCallErrorEventData(LlmErrorEventData):
    pass

@dataclass
class AgentFinishedEventData:
    messages: List[Dict]
