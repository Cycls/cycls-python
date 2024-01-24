from enum import Enum, auto
from pydantic import BaseModel, field_validator
from typing import Any 
from sarya import UI 
from datetime import datetime 

class InputTypeHint(Enum):
    EMPTY = auto()
    MESSAGE = auto()
    CONVERSATION_ID = auto()
    USER = auto()
    SESSION = auto()
    FULL = auto()

class MessageRole(Enum):
    ASSISTANT = "ASSISTANT"
    USER = "user"
    SARYA = "sarya"

class Message(BaseModel):
    id: str
    created_at: datetime 
    content: UI.Text | UI.Image | None
    role: MessageRole = MessageRole.ASSISTANT.value
    meta: dict[str, Any] | None = None

    
    @field_validator("content", mode="before")
    @classmethod
    def create_content(cls, values: dict[str, Any]) :
        content_type = values.get("type")
        if content_type == "text":
            return UI.Text(**values)
        elif content_type == "image":
            return UI.Image(**values)
        else:
            raise ValueError(f"Unknown content type: {content_type}")


Meta = dict[str, Any] 
ConversationID = str

class ConversationSession(BaseModel):
    id : str

    async def get_history(self):
        return 


class NewMessage(BaseModel):
    message: Message
    session : ConversationSession
    meta: dict[str, Any] | None = None

class Response(BaseModel):
    messages: list[UI.Text| UI.Image]
    meta: dict[str, Any] | None = None