

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

## Features
- **Simple:** One codebase to build and deploy across multiple platforms
- **Monetization built-in**: Quick and easy payment button within the chat
- **Multi-Media and UI Rendering**: Serve users with rich media content and interactive UI elements directly in the chat
- **User Access**: Access to Sarya's fast growing user base
- **Cross-Platform Deployment**: Write once, deploy everywhere. SaryaSDK supports iOS, Android, web, whatsapp, terminal and more
- **Bring Your Own LLM**: Flexibility in LLMs, use OpenAI or open source alternatives
- **Spin Off Your Own App**: Utilize our client SDKs to develop your own Sarya experinces on the web/iOS/whatsapp..etc




