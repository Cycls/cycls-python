from __future__ import annotations
from pydantic import PrivateAttr, computed_field, BaseModel, SerializeAsAny
from enum import Enum
from typing import Any

class UITypes(str, Enum):
    Text = "Text"
    Cards = "Cards"
    Pay = "ApplePay"
    Card = "Card"
    HStack = "HStack"
    VStack = "VStack"
    Image = "Image"



class BaseUI(BaseModel):
    content: Any
    
    @computed_field
    @property
    def type(self) -> UITypes:
        return self._type
    def __init__(self, *args, **kwargs):
        if args:
            kwargs["content"] = args[0]
        super().__init__(**kwargs)

            
class Text(BaseUI):
    _type = PrivateAttr(UITypes.Text)
    content: str
    size:int |None = None
    color:str |None = None 

class Payment(BaseUI):
    _type = PrivateAttr(UITypes.Pay)
    content: None = None
    amount: int
    tax : int | None = None
    curency: str|None = "SAR"
    countryCod:str|None = "KSA"




class HStack(BaseUI):
    _type = PrivateAttr(UITypes.HStack)
    content: list[SerializeAsAny[BaseUI]]

class VStack(BaseUI):
    _type = PrivateAttr(UITypes.VStack)
    content: list[SerializeAsAny[BaseUI]]

class Image(BaseUI):
    _type = UITypes.Image
    content : str
    width:int | None = None
    height:int | None = None
    padding: int | None = None
class Card(BaseUI):
    _type = PrivateAttr(UITypes.Card)
    content: list[SerializeAsAny[BaseUI]]
    cornerRedius: int | None = None

class Cards(BaseUI):
    _type = PrivateAttr(UITypes.Cards)
    content: list[Card]
    cornerRedius: int | None = None