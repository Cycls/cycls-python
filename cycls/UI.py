from __future__ import annotations
from enum import Enum
from typing import Any

from pydantic import BaseModel

class UITypes(str, Enum):
    Text = "text"
    Image = "image"

class Text(BaseModel):
    text: str
    type:UITypes = UITypes.Text
    meta:dict[str, Any] | None = None

    def __init__(self, text:str, type:UITypes = UITypes.Text, meta=None):
        super().__init__(text=text, meta=meta)

class Image(BaseModel):
    image : str
    type :UITypes = UITypes.Image
    meta : dict[str, Any] | None = None

    def __init__(self, image_url:str, type:UITypes = UITypes.Image, meta=None):
        super().__init__(Image=image_url, meta=meta)

