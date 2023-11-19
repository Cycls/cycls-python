from sarya import SaryaClient, UI
SaryaClient.token = "<JWT Token>"
sarya = SaryaClient("test", name="test", description="Test")
def main():
    return [UI.Text("Hello World"), UI.Image("https://i.imgur.com/3QXm2oK.jpeg")]
sarya.run(port=8001)

