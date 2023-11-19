from sarya import SaryaClient, UI
SaryaClient.token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHBpcmVzX2luIjoiMjA4My0xMS0wNFQwNjo0OTo0Mi4yOTUxMzkiLCJoYW5kbGVyIjoidGVzdCIsInVybCI6Imh0dHA6Ly8wLjAuMC4wOjgwMDEvIn0.7la-PgJv4nyTta7FP3MRndMFGtr11CgkYJLqBTh0cVo"
sarya = SaryaClient("test", name="test", description="Test")
def main():
    return [UI.Text("Hello World"), UI.Image("https://i.imgur.com/3QXm2oK.jpeg")]
sarya.run(port=8001)

