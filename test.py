from sarya import Sarya, UI, AppConfiguration
from sarya.typings import ConversationSession

client = Sarya("sk-123")

@client.app("@hello_Khalid2")
def hello_02483733(x:ConversationSession):
    return UI.Text("Hello Umair!")


client.run()
