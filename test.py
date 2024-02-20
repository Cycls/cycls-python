from sarya import Sarya, UI
from sarya.typings import ConversationSession

client = Sarya("sk-123")


@client.app("@hello-shah", description="This is some description")
def hello_shah(x:ConversationSession):
    return UI.Text("Hello Shah!")


client.run()
