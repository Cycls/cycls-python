from fastapi import FastAPI, Request
import uvicorn
import UI

class AIRequest:
    def __init__(self) -> None:
        pass
    
    async def __call__(self, request:Request):
        self.request = request
        self.j = await request.json()
        return self
    
    @property
    def messages(self):
        print(self.j)
        return self.j["messages"]
    
    



class SaryaClient:
    token: str | None = None
    def __init__(self,
        name:str|None = None,
        description:str|None = None,
        version:str|None = None,
        ):
        self.name = name
        self.description = description
        self.version = version
        self._set_app()

    

    def run(self, host: str = "0.0.0.0", port: int = 8000):
        uvicorn.run(self.app, host=host, port=port)

    def _set_app(self):
        self.app = FastAPI(title=self.name, description=self.description, version=self.version)
        self.app.on_event("startup")(self._startup)
        self.app.on_event("shutdown")(self._shutdown)
        self.app.post("/check")(self._check)
    
    def main(self, func):
        # add func to be post route
        self.app.post("/main")(func)
    
    def _startup(self):
        # I am active 
        print("Sarya is running...")

    
    def _shutdown(self):
        print("Sarya is shutting down...")

    def _check(self):
        return {"status": "ok"}

if __name__ == "__main__":
    SaryaClient.token = "test-token"
    
    sarya = SaryaClient(nmae="Test", description="Test", version="0.0.1")

    # @sarya.on_startup
    # async def startup():


    @sarya.main
    async def main():
        # history that are related to you 
        # a way to add more history items 
        # you do your thing
        return UI.Text("Hello World")
    
    # @sarya.on_shutdown
    # async def shutdown():

    sarya.run()




    
        


