

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
from sarya import SaryaClient, UI

sarya = SaryaClient(name="hello",description="hello world marid",
                    url="https://link.to.your.app")

def main(x):
    return UI.Text("Hello World!")

sarya.run()
```
