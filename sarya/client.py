from fastapi import FastAPI, Request
import uvicorn
import httpx
from pydantic import BaseModel 

from typing import Any
from functools import partial
import inspect 
import importlib 

from sarya import UI
from .constant import SARYA_URL

class NewMessage(BaseModel):
    messages: list[dict[str, Any]] 
    meta: dict[str, Any] | None = None

class Response(BaseModel):
    messages: list[UI.Text| UI.Image]
    meta: dict[str, Any] | None = None

class AIRequest:
    def __init__(self) -> None:
        pass
    
    async def __call__(self, request:Request):
        self.request = request
        self.j = await request.json()
        return self
    
    @property
    def messages(self):
        print(self.j)
        return self.j["messages"]
    
    



class SaryaClient:
    token: str | None = None

    def __init__(self,
        handler:str,*,
        name:str|None ,
        description:str|None = None,
        version:str|None = None
        ):
        """

        """
        self.handler = handler
        self.name = name
        self.description = description or "No description provided"
        self.version = version or "0.0.1"
        self._set_app()


    

    def run(self, main:str|None="main", host: str = "0.0.0.0", port: int = 8000):
        caller_frame = inspect.currentframe().f_back
        caller_module_info = inspect.getmodule(caller_frame)
        if caller_module_info is not None:
            caller_module_name = caller_module_info.__name__
            module = importlib.import_module(caller_module_name)
    
            main_func = getattr(module, main)
            self.main_function = main_func
            self.app.post("/main")(self.main)
            uvicorn.run(self.app, host=host, port=port)
        else:
            raise Exception("Could not find main function")



    def _set_app(self):
        self.app = FastAPI(title=self.name, description=self.description, version=self.version)
        self.app.on_event("startup")(self._startup)
        self.app.get("/")(self._check)
        self.app.on_event("shutdown")(self._shutdown)
    
    def main(self, payload:NewMessage):
        # add func to be post route
        if (params:=len(inspect.signature(self.main_function).parameters)) == 2:
            output = self.main_function(payload.messages, payload.meta)
        elif params == 1:
            output = self.main_function(payload.messages)
        else:
            output = self.main_function()
        if isinstance(output, Response):
            return output
        elif isinstance(output, UI.Text) or isinstance(output, UI.Image):
            return Response(messages=[output])
        elif isinstance(output, list):
            return Response(messages=output)
        return Response(**output)

    
    async def _startup(self):
        async with httpx.AsyncClient() as client:
            url = SARYA_URL + f"marid/{self.handler}/on"
            headers = {"x-marid-auth": self.token}
            response = await client.post(url, json={"name": self.name, "description": self.description}, headers=headers)
        response.raise_for_status()
        print("Sarya is running...")

    

    async def _shutdown(self):
        async with httpx.AsyncClient() as client:
            url = SARYA_URL + f"marid/{self.handler}/off"
            headers = {"x-marid-auth": self.token}
            await client.post(url, json={"name": self.name, "description": self.description}, headers=headers)
        print("Sarya is shutting down...")

    async def _check(self):
        return {"data":{"status": "OK"}}






    
        


