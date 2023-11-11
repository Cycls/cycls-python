from fastapi import FastAPI, Request
import uvicorn
import httpx
from typing import Any
from functools import partial
import inspect 
import importlib 

from sarya import UI
from pydantic import BaseModel 

class Response(BaseModel):
    message: UI.Text
    meta: dict[str, Any] | None = None

class NewMessage(BaseModel):
    messages: list[dict[str, Any]] | None = None
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
    sarya_url = "https://saryahai.ikhalid-alrashe.repl.co"
    def __init__(self,
        name:str|None = None,
        description:str|None = None,
        version:str|None = None,
        url:str|None = "http://0.0.0.0:8000",
        ):
        self.name = name
        self.description = description
        self.version = version
        self.url = url
        self._set_app()


    

    def run(self, main:str|None="main", host: str = "0.0.0.0", port: int = 8000):
        caller_frame = inspect.currentframe().f_back
        caller_module_info = inspect.getmodule(caller_frame)
        if caller_module_info is not None:
            caller_module_name = caller_module_info.__name__
            module = importlib.import_module(caller_module_name)
    
            main_func = getattr(module, "main")
            self.main_function = main_func
            self.app.post("/main")(self.main)
            uvicorn.run(self.app, host=host, port=port)
        else:
            raise Exception("Could not find main function")


    def _set_app(self):
        self.app = FastAPI(title=self.name, description=self.description, version=self.version)
        self.app.on_event("startup")(self._startup)
        self.app.get("/health_check")(self._check)
        self.app.on_event("shutdown")(self._shutdown)
    
    def main(self, payload:NewMessage):
        # add func to be post route
        if (params:=len(inspect.signature(self.main_function).parameters)) == 2:
            print("Params 2")
            output = self.main_function(payload.messages, payload.meta)
        elif params == 1:
            print("Params 1")
            output = self.main_function(payload.messages)
        else:
            print("No params")
            output = self.main_function()
        if isinstance(output, Response):
            return output
        elif isinstance(output, UI.Text):
            output = Response(message=output)
        return Response(**output)

    
    async def _startup(self):
        async with httpx.AsyncClient() as client:
            url = SaryaClient.sarya_url + "/sdk/marid"
            print(f"Sending request to {url}")
            response = await client.post(url, json={"name": self.name, "description": self.description, "url": self.url})
        print(response.text)  
        print("Sarya is running...")

    
    async def _shutdown(self):
        async with httpx.AsyncClient() as client:
            await client.post(SaryaClient.sarya_url + "/sdk/marid/off", json={"name": self.name, "description": self.description, "url": self.url})
        print("Sarya is shutting down...")

    def _check(self):
        return {"status": "ok"}






    
        


