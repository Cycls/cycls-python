from sarya import Sarya, UI, AppConfiguration
from sarya.typings import ConversationSession

client = Sarya("sk-123")
config = AppConfiguration()

@client.app("@hello_Khalid2", config=config)
def hello_02483733(x:ConversationSession):
    hist = x.get_history()
    return UI.Text("Hello Umair!")


client.run()
