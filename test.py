from cycls import Cycls, UI
from cycls.typings import Message, UserMessage
from asyncio import sleep

client = Cycls("sk-123")


@client.app("@hi")
async def hello_shah(x:UserMessage):
    async with x.stream.text() as text:
        for w in ["Hi", ", ", "I am", "Khalid"]:
            await text(w)
            await sleep(1)
    await x.send.text("Hi there again")


client.publish()
