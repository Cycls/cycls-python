

<p align="center">
<a href="https://sarya.com"><img src="https://github.com/Cycls/SaryaSDK/assets/58256600/b2308cba-4777-4f37-bf1e-e1106412ecee" alt="SaryaSDK logo"></a>
</p>

<p align="center">
<b>SaryaSDK - the universal access layer</b>
<br/><br/>
The fastest way to build and publish Sarya LLM apps ⚡️
</p>

<p align="center">
<a href="https://sarya.com/docs" target="_blank"> Docs </a>
|
<a href="https://sarya.com" target="_blank"> Homepage </a>
</p>

```bash
pip install sarya-sdk
```

## Example

```python
from sarya import SaryaClient, UI, SaryaResponse
from fastapi import Request


if __name__ == "__main__":
    SaryaClient.token = "test-token"
    
    sarya = SaryaClient(
            name="Test",
            description="Test",
            version="0.0.1",
            url="https://www.xxxx.com"
          )

    @sarya.main
    async def main(request:Request):
        body = await request.body()

        # ---------
        # your logic
        # ---------
        
        return SaryaResponse(message = UI.Text("Hello World"), meta={}) # you can add anything in meta
    
    sarya.run()
```
