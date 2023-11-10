from sarya import SaryaClient, UI, SaryaResponse
from fastapi import Request


if __name__ == "__main__":
    SaryaClient.token = "test-token"
    
    sarya = SaryaClient(name="Test", description="Test", version="0.0.1", url="http://0.0.0.0:8001")

    # @sarya.on_startup
    # async def startup():


    @sarya.main
    async def main(request:Request):
        body = await request.body()
        print(body)
        # history that are related to you 
        # a way to add more history items 
        # you do your thing
        return SaryaResponse(message = UI.Text("Hello World"))
    


    sarya.run(port=8001)