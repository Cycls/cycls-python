from cycls import Cycls, UI
from cycls.typings import Message, UserMessage
from asyncio import sleep

client = Cycls("sk-123")


@client.app("@hi",
    name="Testing Hi",
    image="https://media.licdn.com/dms/image/D4D0BAQHuqwI-bbCOKA/company-logo_100_100/0/1708092754484/cycls_logo?e=1718841600&v=beta&t=XORYFWYp3F_tgjmWU2kTZfCa1YKMixdV-ed9z7VDD94",
    suggestions=["hi there", "who are you?"],
    introduction="""
# this is a header
```
this is a code
```
""")
async def hello_shah(x:UserMessage):
    async with x.stream.text() as text:
        for w in ["Hi", ", ", "I am", "Khalid"]:
            await text(w)
            await sleep(1)
    await x.send.text("Hi there again")


client.publish()
