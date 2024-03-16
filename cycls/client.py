from __future__ import annotations
from inspect import iscoroutinefunction, signature, Parameter, _empty
from typing import Callable, Any
from datetime import datetime


from socketio import AsyncClient
import asyncio
import re

from .UI import Text, Image
from .configuration import AppConfiguration
from .typings import (
    InputTypeHint,
    UserMessage,
    ConversationID,
    ConversationSession,
    Meta,
    Response,
    Message,
    MessageContent
)
from .static import HANDLER_PATTERN, CYCLS_URL


class Cycls:
    def __init__(self, key: str | None = None):
        self.key = key
        self.sio = AsyncClient(
            reconnection_attempts=0,
            reconnection_delay=1,
            reconnection_delay_max=25,
            logger=True,
        )
        self.apps_config: list[AppConfiguration] = []
        self.sio.on("connect")(self.re_connect)
        self.sio.on("connection_log")(self.connection_log)


    async def re_connect(self):
        for app in self.apps_config:
            await self.sio.emit("connect_app", data=app.model_dump(mode="json"))
        print("CONNECTING")


    async def _run(self):
        headers = {
            "x-dev-secret": self.key,
        }
        await self.sio.connect(
            CYCLS_URL,
            headers=headers,
            transports=["websocket"],
            socketio_path="/app-socket/socket.io",
        )
        await self.sio.wait()


    def publish(self):
        asyncio.run(self._run())

    def _process_response(self, response):
        if isinstance(response, Response):
            return response
        elif isinstance(response, Text) or isinstance(response, Image):
            return Response(messages=[response])
        elif isinstance(response, list):
            return Response(messages=response)
        return Response(messages=[response])

    def _parameter_type_hint(self, param: Parameter) -> InputTypeHint:
        hint = param.annotation
        mapping = {
            _empty: InputTypeHint.EMPTY,
            Message: InputTypeHint.MESSAGE,
            ConversationSession: InputTypeHint.SESSION,
            ConversationID: InputTypeHint.CONVERSATION_ID,
            UserMessage: InputTypeHint.FULL,
            MessageContent: InputTypeHint.MESSAGE_CONTENT,
        }
        if output := mapping.get(hint):
            return output
        else:
            raise Exception("")

    def _get_parameter_value(self, hint: InputTypeHint, obj: user_message) -> Any:
        if  hint == InputTypeHint.MESSAGE_CONTENT:
            return obj.message.content
        elif hint == InputTypeHint.SESSION:
            return obj.session
        elif hint == InputTypeHint.CONVERSATION_ID:
            return obj.session.id
        elif hint == InputTypeHint.MESSAGE:
            return obj.message
        elif hint == InputTypeHint.USER:
            return None
        elif hint == InputTypeHint.EMPTY or hint == InputTypeHint.FULL:
            return obj

    def process_handler_input(self, func: Callable, message: UserMessage):
        kwargs = {}
        for key, value in signature(func).parameters.items():
            type_hint = self._parameter_type_hint(value)
            kwargs[key] = self._get_parameter_value(hint=type_hint, obj=message)
        return kwargs

    def extract_handler_name(self, handler: str) -> str:
        name = re.search(rf"^\@({HANDLER_PATTERN})$", handler.strip().lower())
        if not name:
            raise Exception(
                "Your app handler has to start with @ and composed only of letters, numbers and '-'"
            )
        name = name.group(1)
        return re.sub(r"_", "-", name)

    def app(
        self,
        handler: str,
        name: str | None = None,
        image: str | None = None,
        introduction: str| None = None,
        suggestions: list[str] | None = None
    ):
        """ """
        app_handler = self.extract_handler_name(handler)
        config = AppConfiguration(
            handler=app_handler,
            name=name,
            image=image,
            introduction=introduction,
            suggestions=suggestions

        )

        def decorator(func):
            self.apps_config.append(config)

            @self.sio.on(app_handler)
            async def wrapper(data):
                try:
                    message = UserMessage(sio=self.sio, **data)
                except Exception as e:
                    print(e)
                    print(f"we got error while trying to process {data}")
                    return Response(messages=[Text("something went wrong")]).model_dump(
                        mode="json"
                    )

                await func(**self.process_handler_input(func, message))
                await message.send.send_message(None, message.send.user_message_id, True, "finish")
                return 200

            return wrapper

        return decorator

    async def connection_log(self, data):
        print(
            f"{datetime.now()}: HANDLER|{data.get('handler')} -> {data.get('message')}. STATUS: {data.get('status')}"
        )
