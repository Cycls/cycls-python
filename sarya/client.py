from __future__ import annotations
from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import JSONResponse
import uvicorn

import inspect
import importlib

from sarya import UI
from sarya.request_typings import NewMessage, Response
from sarya.signature import HMAS


class AIRequest:
    def __init__(self) -> None:
        pass

    async def __call__(self, request: Request):
        self.request = request
        self.j = await request.json()
        return self

    @property
    def messages(self):
        return self.j["messages"]



class Sarya:

    def __init__(self, key: str | None = None):
        self.key = key
        self._set_app()

    def run(self, main: str | None = "main", host: str = "0.0.0.0", port: int = 8000):
        caller_frame = inspect.currentframe().f_back
        caller_module_info = inspect.getmodule(caller_frame)
        if caller_module_info is not None:
            caller_module_name = caller_module_info.__name__
            module = importlib.import_module(caller_module_name)

            main_func = getattr(module, main)
            self.main_function = main_func
            self.app.post("/main")(self.main)
            app = FastAPI()
            app.include_router(self.app)
            uvicorn.run(app, host=host, port=port)
        else:
            raise Exception("Could not find main function")

    def _set_app(self):
        self.app = APIRouter()
        self.app.get("/subscribe")(self._subscribe)

    async def main(self, request:Request, payload: NewMessage):
        try:
            await self._hmas(request)
        except Exception as e:
            return JSONResponse(
                {"error": "request was not sign correctly"}, status_code=401
            )
        if (params := len(inspect.signature(self.main_function).parameters)) == 2:
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
        return Response(messages=[output])

    async def _subscribe(self, request: Request):
        try:
            await self._hmas(request)
        except Exception as e:
            return JSONResponse(
                {"error": "request was not sign correctly"}, status_code=401
            )
        return {"data": {"secret": self.key}}

    async def _hmas(self, request: Request):
        sign = await HMAS.verify(self.key, request)
        if sign:
            return True
        else:
            raise Exception("Request was not signed correctly")
