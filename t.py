from sarya import SaryaClient, UI
SaryaClient.token = "test-token"
sarya = SaryaClient(name="Test", description="Test", url="http://0.0.0.0:8001")
def main():
    return UI.Text("Hello World")
sarya.run(port=8001)