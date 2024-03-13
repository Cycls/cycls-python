from enum import Enum, auto
from pydantic import BaseModel, field_validator
from typing import Any, TypeVar
from cycls import UI
from datetime import datetime
from socketio import AsyncClient
import uuid
from contextlib import asynccontextmanager

MessageContent = TypeVar('MessageContent',bound=UI.Text| UI.Image| None)
class InputTypeHint(Enum):
    EMPTY = auto()
    MESSAGE = auto()
    CONVERSATION_ID = auto()
    USER = auto()
    SESSION = auto()
    FULL = auto()
    MESSAGE_CONTENT = auto()

class MessageRole(Enum):
    ASSISTANT = "ASSISTANT"
    USER = "user"
    CYCLS = "cycls"

class Message(BaseModel):
    id: str
    created_at: datetime
    content: MessageContent
    role: MessageRole = MessageRole.ASSISTANT
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





class Response(BaseModel):
    messages: list[UI.Text| UI.Image]
    meta: dict[str, Any] | None = None

class send_base:
    def __init__(self, sio:AsyncClient, user_message_id) -> None:
        self.sio = sio
        self.user_message_id = user_message_id
    async def send_message(self, content, id, stream:bool=False, finish_reason:str|None=None):
        if isinstance(content, BaseModel):
            content = content.model_dump(mode="json", exclude_none=True)
        await self.sio.emit(
            "response",
            {
                "content":content,
                "id": id,
                "user_message_id": self.user_message_id,
                "finish_reason": finish_reason,
                "stream":stream
            },
        )
class Send(send_base):
    async def text(self, message):
        id = str(uuid.uuid4())
        content = UI.Text(text=message)
        await self.send_message(content=content, id=id)

class SendStream(send_base):
    @asynccontextmanager
    async def text(self):
        id = str(uuid.uuid4())

        async def send(chunk):
            await self.send_message(UI.Text(text=chunk), id, True)

        try:
            yield send
        except:
            await self.send_message(None, id, True, "error")
        finally:
            pass

class userMessage(BaseModel):
    message: Message
    session : ConversationSession
    meta: dict[str, Any] | None = None


class UserMessage:
    message: Message
    session : ConversationSession
    meta: dict[str, Any] | None = None
    send:Send
    stream:SendStream
    def __init__(self, message, session, meta, sio):
        m = userMessage(message=message, session=session, meta=meta)
        self.message = m.message
        self.session = m.session
        self.meta = m.meta
        self.send = Send(sio=sio, user_message_id=self.message.id)
        self.stream = SendStream(sio=sio, user_message_id=self.message.id)
