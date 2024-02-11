<!-- 
<p align="center">
<img style="height: 75px;" src="https://www.sarya.com/img/logo.svg" alt="logo" />
</p>
-->

<p align="center">
<b>Cycls - Generative UI for your AI</b>
<br/><br/>
Design, publish, and share end user AI apps with Cycls ⚡️
</p>

<div align="center">
    <a href="https://discord.gg/BMnaMatDC7" target="_blank" rel="noopener noreferrer">
        <img loading="lazy" src="https://img.shields.io/discord/1175782747164389466" alt="Discord" class="img_ev3q" style="display: inline;">
    </a>
    <a href="https://GitHub.com/cycls/sarya-python/stargazers/" target="_blank" rel="noopener noreferrer">
        <img loading="lazy" src="https://img.shields.io/github/stars/cycls/sarya-python.svg?style=social&label=Star&maxAge=2400" alt="GitHub stars" class="img_ev3q" style="display: inline;">
    </a>
</div>

<p align="center">
<a href="https://sarya.com/docs" target="_blank"> Docs </a>
|
<a href="https://sarya.com" target="_blank"> Homepage </a>
|
<a href="https://platform.sarya.com" target="_blank"> Platform </a>
</p>

```bash
pip install sarya
```

## Example

```python
from cycls import Cycls, UI

client = Cycls("SECRET")

@client.app("@my-app")
def app():
    return UI.Text("Hello World!")

client.run()
```

## Features
- **100% control over your code**: Maintain your app logic and data on your infrastructure.
- **Bring your own LLM**: Flexibility in LLMs, use OpenAI or any open source alternative.
- **Generative UI**: Quickly generate rich UIs that integrate seamlessly with your AI logic.
- **Instant sharing**: Instantly share your customer-facing AI app.
- **Data & analytics**: Measure app's performance. Use data to finetune AI for better results.
- **Cross-platform**: Sarya currently is web-based. Mobile support for iOS and Android is underway.
- **Multimodal I/O**: Starting with text input, and expanding to voice, image, and video data inputs.

## Generative UI?

**Generative UI** (User Interface) is simply when AI is constantly designing and improving user interfaces in response to dynamic user behavior. Generative UIs are an upgrade in UI development, mirroring the rise of generative AI.
