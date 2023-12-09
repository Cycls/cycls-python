from __future__ import annotations
from pydantic import BaseModel
from enum import Enum
from typing import Any

class UITypes(str, Enum):
    Text = "text"
    Image = "image"

class Text(BaseModel):
    type:UITypes = UITypes.Text
    content: str
    def __init__(self, content: str) -> None:
        super().__init__(content=content, type=UITypes.Text)
class Image(BaseModel):
    type:UITypes = UITypes.Image
    content : str
    def __init__(self, content: str) -> None:
        super().__init__(content=content, type=UITypes.Image)

