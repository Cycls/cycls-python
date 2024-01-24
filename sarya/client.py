from __future__ import annotations
from inspect import iscoroutinefunction, signature, Parameter, _empty
from typing import Callable, Any 
from datetime import datetime
import logging 

from socketio import AsyncClient
import asyncio
import re

from .UI import Text, Image
from .configuration import AppConfiguration, AppNameLocale, ImageUploader
from .typings import InputTypeHint, NewMessage, ConversationID, ConversationSession, Meta, Response, Message

HANDLER_PATTERN = "[a-zA-Z][a-zA-Z0-9_-]{0,25}"


class Sarya:
    def __init__(self, key: str | None = None, log_level="info", logger:bool=False):
        self.key = key
        self.sio = AsyncClient(
            reconnection_attempts=0,
            reconnection_delay=1,
            reconnection_delay_max=25,
            logger=True,
        )
        self.apps_config:list[AppConfiguration] = []
        self.sio.on("connection_log")(self.connection_log)
        self.sio.on("config")(self.get_config)
        self._set_logger(log_level="info", logger=False)

    def _set_logger(self, logger:bool, log_level:str):
        if not logger:
            self.logger = None
            return 
        
    async def _run(self):
        headers = {
            "x-dev-secret": self.key,
        }
        await self.sio.connect(
            # "https://api.sarya.com",
            "http://localhost:8001",
            headers=headers,
            transports=["websocket"],
            socketio_path="/app-socket/socket.io",
        )
        await self.sio.wait()

    def run(self, release:str | None = None):
        if release:
            self._set_global_release(release)
        asyncio.run(self._run())

    def _set_global_release(self, release:str)->None:
        apps = []
        for app in self.apps_config:
            app.release = release
            apps.append(app)
        self.apps_config = apps
    
    def _process_response(self, response):
        if isinstance(response, Response):
            return response
        elif isinstance(response, Text) or isinstance(response, Image):
            return Response(messages=[response])
        elif isinstance(response, list):
            return Response(messages=response)
        return Response(messages=[response])
    
    def _parameter_type_hint(self, param:Parameter) -> InputTypeHint:
        hint = param.annotation
        mapping = {
            _empty: InputTypeHint.EMPTY,
            Message: InputTypeHint.MESSAGE,
            ConversationSession: InputTypeHint.SESSION,
            ConversationID: InputTypeHint.CONVERSATION_ID,
            NewMessage: InputTypeHint.FULL
        }
        if output:= mapping.get(hint):
            return output
        else: 
            raise Exception("")

    def _get_parameter_value(self, hint:InputTypeHint, obj:NewMessage) -> Any:
        if hint == InputTypeHint.EMPTY or hint == InputTypeHint.FULL:
            return obj
        elif hint == InputTypeHint.SESSION:
            return obj.session
        elif hint == InputTypeHint.CONVERSATION_ID:
            return obj.session.id
        elif hint == InputTypeHint.MESSAGE:
            return obj.message
        elif hint == InputTypeHint.USER:
            return None 
        
    def process_handler_input(self, func:Callable, user_message:NewMessage):
        kwargs = {}
        for key, value in signature(func).parameters.items():
            type_hint = self._parameter_type_hint(value)
            kwargs[key] = self._get_parameter_value(hint=type_hint, obj=user_message)
        return kwargs

    def extract_handler_name(self, handler: str) -> str | None:
        name = re.search(rf"^\@({HANDLER_PATTERN})$", handler.strip().lower())
        if not name:
            raise Exception(
                "Your app handler has to start with @ and composed only of letters, numbers and '-'"
            )
        name = name.group(1)
        return re.sub(r"_", "-", name)

    def app(self, 
            handler:str,
            name: str | AppNameLocale = None,
            test: bool = False,
            image: str | ImageUploader = None, 
            release: str | None = None,
            description: str = None
        ):
        """
        """
        app_handler = self.extract_handler_name(handler)
        config = AppConfiguration(
            handler=handler,
            name=name,
            test=test,
            image=image,
            release=release,
            description=description
        )

        def decorator(func):
            self.apps_config.append(config)
            
            @self.sio.on(app_handler)
            async def wrapper(data):
                try:
                    user_message = NewMessage(**data)
                except Exception as e:
                    print(e)
                    print(f"we got error while trying to process {data}")
                    return Response(messages=[Text("something went wrong")]).model_dump(
                        mode="json"
                    )
                if iscoroutinefunction(func):
                    response = await func(
                        **self.process_handler_input(func, user_message)
                    )
                else:
                    response = func(**self.process_handler_input(func, user_message))
                return self._process_response(response).model_dump(mode="json")

            return wrapper

        return decorator

    async def connection_log(self, data):
        print(
            f"{datetime.now()}: HANDLER|{data.get('handler')} -> {data.get('message')}. STATUS: {data.get('status')}"
        )

    async def get_config(self):
        return [c.model_dump(mode="json") for c in self.apps_config]