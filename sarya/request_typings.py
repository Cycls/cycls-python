from pydantic import BaseModel

from typing import Any

from sarya import UI

class NewMessage(BaseModel):
    messages: list[dict[str, Any]] 
    meta: dict[str, Any] | None = None

class Response(BaseModel):
    messages: list[UI.Text| UI.Image]
    meta: dict[str, Any] | None = None