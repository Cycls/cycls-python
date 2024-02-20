import httpx
import asyncio








async def main():
    with httpx.stream(
        "POST",
        "http://0.0.0.0:8004/stream",
        json={"body": {"type": "text", "text": "@hello-shah hi"}, "meta": {}},
        timeout=100
    ) as response:
        for chunk in response.iter_bytes(chunk_size=1):
            if chunk:
                print(chunk.decode(), end="", flush=True)


asyncio.run(main())
